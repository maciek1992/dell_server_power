import logging
import paramiko
from homeassistant.helpers.entity import Entity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN, CONF_IDRAC_IP, CONF_IDRAC_USERNAME, CONF_IDRAC_PASSWORD, CONF_PRICE_PER_KWH

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Konfiguracja czujników z UI"""
    config = entry.data
    sensor = DellServerPowerSensor(
        config[CONF_IDRAC_IP],
        config[CONF_IDRAC_USERNAME],
        config[CONF_IDRAC_PASSWORD],
        config.get(CONF_PRICE_PER_KWH, 0.75),  # Domyślna cena za kWh
    )
    
    async_add_entities([sensor], update_before_add=True)

class DellServerPowerSensor(Entity):
    """Sensor pobierający dane o zużyciu prądu z iDRAC"""

    def __init__(self, idrac_ip, username, password, price_per_kwh):
        self._idrac_ip = idrac_ip
        self._username = username
        self._password = password
        self._price_per_kwh = price_per_kwh
        self._state = None
        self._attributes = {}

    def update(self):
        """Pobranie danych przez SSH"""
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self._idrac_ip, username=self._username, password=self._password)
            stdin, stdout, stderr = ssh.exec_command("racadm get system.Power")
            output = stdout.read().decode()
            ssh.close()

            for line in output.split("\n"):
                if "Realtime.Power=" in line:
                    self._state = float(line.split("=")[1].strip().split()[0])

                if "EnergyConsumption=" in line:
                    total_energy_kwh = float(line.split("=")[1].strip().split()[0])
                    self._attributes["total_energy_kwh"] = total_energy_kwh
                    self._attributes["total_cost"] = round(total_energy_kwh * self._price_per_kwh, 2)

            if self._state:
                daily_energy_kwh = (self._state / 1000) * 24
                monthly_energy_kwh = daily_energy_kwh * 30
                self._attributes["daily_cost"] = round(daily_energy_kwh * self._price_per_kwh, 2)
                self._attributes["monthly_cost"] = round(monthly_energy_kwh * self._price_per_kwh, 2)
                self._attributes["price_per_kwh"] = self._price_per_kwh

        except Exception as e:
            _LOGGER.error(f"Błąd pobierania danych z iDRAC: {e}")

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes