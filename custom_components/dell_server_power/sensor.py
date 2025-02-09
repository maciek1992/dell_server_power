import logging
import paramiko
import paho.mqtt.client as mqtt
from homeassistant.helpers.entity import Entity
from .const import DOMAIN, CONF_IDRAC_IP, CONF_IDRAC_USERNAME, CONF_IDRAC_PASSWORD, CONF_MQTT_SERVER, CONF_MQTT_PORT, CONF_MQTT_USERNAME, CONF_MQTT_PASSWORD, CONF_COST_PER_KWH

_LOGGER = logging.getLogger(__name__)

def get_power_usage_ssh(ip, username, password):
    """ Pobiera zużycie energii z iDRAC przez SSH """
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=username, password=password, timeout=5)
        stdin, stdout, stderr = client.exec_command("racadm get system.Power")
        output = stdout.read().decode()
        client.close()

        _LOGGER.debug(f"Output from iDRAC:\n{output}")  # Debugowanie odpowiedzi

        for line in output.split("\n"):
            if "Realtime.Power" in line:
                return int(line.split("=")[1].strip().split(" ")[0])  # Pobiera wartość w Watach

    except Exception as e:
        _LOGGER.error(f"Error fetching power data from Dell via SSH: {e}")
        return None

    return None

class DellServerPowerSensor(Entity):
    """ Sensor do odczytu zużycia energii """

    def __init__(self, idrac_ip, username, password):
        self._idrac_ip = idrac_ip
        self._username = username
        self._password = password
        self._state = None
        self._attr_native_unit_of_measurement = "W"

    def update(self):
        """ Pobiera dane o zużyciu energii """
        self._state = get_power_usage_ssh(self._idrac_ip, self._username, self._password)

    @property
    def name(self):
        return "Dell Server Power Usage"

    @property
    def state(self):
        return self._state

class DellServerCostSensor(Entity):
    """ Sensor do wyliczania kosztu energii """

    def __init__(self, idrac_ip, username, password, cost_per_kwh):
        self._idrac_ip = idrac_ip
        self._username = username
        self._password = password
        self._cost_per_kwh = cost_per_kwh
        self._state = None
        self._attr_native_unit_of_measurement = "PLN/min"

    def update(self):
        """ Oblicza koszt energii na podstawie zużycia """
        power_watts = get_power_usage_ssh(self._idrac_ip, self._username, self._password)

        if power_watts is not None and self._cost_per_kwh is not None:
            power_kwh = (power_watts / 1000) * (1 / 60)  # Przeliczenie na kWh dla minuty
            self._state = round(power_kwh * self._cost_per_kwh, 4)  # Koszt za minutę
        else:
            _LOGGER.error("Nie można obliczyć kosztu energii - brak danych")

    @property
    def name(self):
        return "Dell Server Power Cost"

    @property
    def state(self):
        return self._state

async def async_setup_entry(hass, entry, async_add_entities):
    """ Set up Dell Server Power Monitor sensor from a config entry. """
    idrac_ip = entry.data[CONF_IDRAC_IP]
    username = entry.data[CONF_IDRAC_USERNAME]
    password = entry.data[CONF_IDRAC_PASSWORD]
    
    cost_per_kwh = entry.data.get(CONF_COST_PER_KWH, 0.75)  # Domyślna cena za kWh

    async_add_entities([
        DellServerPowerSensor(idrac_ip, username, password),
        DellServerCostSensor(idrac_ip, username, password, cost_per_kwh)
    ], update_before_add=True)