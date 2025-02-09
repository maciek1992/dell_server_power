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
    async_add_entities([DellServerPowerSensor(config)], update_before_add=True)

class DellServerPowerSensor(Entity):
    """Sensor pobierający dane o zużyciu prądu z iDRAC"""

    def __init__(self, config):
        self._idrac_ip = config[CONF_IDRAC_IP]
        self._username = config[CONF_IDRAC_USERNAME]
        self._password = config[CONF_IDRAC_PASSWORD]
        self._price_per_kwh = config.get(CONF_PRICE_PER_KWH, 0.75)
        self._state = None
        self._attr_native_unit_of_measurement = "W"
        self._attr_name = "Dell Server Power Usage"

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

        except Exception as err:
            _LOGGER.error(f"Błąd pobierania danych z iDRAC: {err}")

    @property
    def state(self):
        return self._state
