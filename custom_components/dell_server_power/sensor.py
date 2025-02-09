import logging
import requests
import paho.mqtt.client as mqtt
from homeassistant.helpers.entity import Entity
from .const import DOMAIN, CONF_IDRAC_IP, CONF_IDRAC_USERNAME, CONF_IDRAC_PASSWORD, CONF_MQTT_SERVER, CONF_MQTT_PORT, CONF_MQTT_USERNAME, CONF_MQTT_PASSWORD

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Configure the sensor"""
    idrac_ip = config[CONF_IDRAC_IP]
    username = config[CONF_IDRAC_USERNAME]
    password = config[CONF_IDRAC_PASSWORD]

    mqtt_server = config[CONF_MQTT_SERVER]
    mqtt_port = config.get(CONF_MQTT_PORT, 1883)
    mqtt_user = config.get(CONF_MQTT_USERNAME, "")
    mqtt_pass = config.get(CONF_MQTT_PASSWORD, "")

    add_entities([DellServerPowerSensor(idrac_ip, username, password, mqtt_server, mqtt_port, mqtt_user, mqtt_pass)], True)

class DellServerPowerSensor(Entity):
    """Sensor to fetch power consumption from Dell iDRAC"""

    def __init__(self, idrac_ip, username, password, mqtt_server, mqtt_port, mqtt_user, mqtt_pass):
        self._idrac_ip = idrac_ip
        self._username = username
        self._password = password
        self._mqtt_server = mqtt_server
        self._mqtt_port = mqtt_port
        self._mqtt_user = mqtt_user
        self._mqtt_pass = mqtt_pass
        self._state = None
        self._attr_native_unit_of_measurement = "W"

    def update(self):
        """Fetch power consumption from iDRAC and send to MQTT"""
        url = f"https://{self._idrac_ip}/data?set=power"
        try:
            response = requests.get(url, auth=(self._username, self._password), verify=False, timeout=5)
            data = response.json()
            self._state = data.get("power", 0)
            
            # Send to MQTT
            client = mqtt.Client()
            if self._mqtt_user:
                client.username_pw_set(self._mqtt_user, self._mqtt_pass)
            client.connect(self._mqtt_server, self._mqtt_port, 60)
            client.publish("homeassistant/sensor/dell_r620_power", str(self._state))
            client.disconnect()

        except Exception as e:
            _LOGGER.error(f"Error fetching power data from Dell: {e}")
            self._state = None

    @property
    def name(self):
        return "Dell Server Power Usage"

    @property
    def state(self):
        return self._state

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the sensor platform from a config entry."""
    async_add_entities([DellPowerSensor(hass, entry)], update_before_add=True)