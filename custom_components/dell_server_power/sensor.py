import logging
import paramiko
from homeassistant.helpers.entity import Entity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN, CONF_IDRAC_IP, CONF_IDRAC_USERNAME, CONF_IDRAC_PASSWORD

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Konfiguracja sensora po dodaniu integracji"""
    config = entry.data
    sensor = DellServerPowerSensor(
        config[CONF_IDRAC_IP],
        config[CONF_IDRAC_USERNAME],
        config[CONF_IDRAC_PASSWORD]
    )
    
    async_add_entities([sensor], update_before_add=True)

class DellServerPowerSensor(Entity):
    """Sensor pobierający dane o zużyciu prądu z iDRAC"""

    def __init__(self, idrac_ip, username, password):
        self._idrac_ip = idrac_ip
        self._username = username
        self._password = password
        self._state = None
        self._attr_native_unit_of_measurement = "W"
        self._attr_name = "Dell Server Power Usage"
        self._attr_unique_id = "dell_server_power_usage"

    def update(self):
        """Pobranie danych o zużyciu energii przez SSH"""
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self._idrac_ip, username=self._username, password=self._password)
            stdin, stdout, stderr = ssh.exec_command("racadm get system.Power")
            output = stdout.read().decode()
            ssh.close()

            for line in output.split("\n"):
                if "Realtime.Power=" in line:
                    power_value = float(line.split("=")[1].strip().split()[0])
                    self._state = f"{power_value:.1f}W"  # Format jako "xx,xW"

        except Exception as e:
            _LOGGER.error(f"Błąd pobierania danych z iDRAC: {e}")

    @property
    def state(self):
        return self._state