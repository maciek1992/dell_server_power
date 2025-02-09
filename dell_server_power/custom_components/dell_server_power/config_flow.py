import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CONF_IDRAC_IP, CONF_IDRAC_USERNAME, CONF_IDRAC_PASSWORD, CONF_MQTT_SERVER, CONF_MQTT_PORT, CONF_MQTT_USERNAME, CONF_MQTT_PASSWORD, DEFAULT_MQTT_PORT

class DellServerPowerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Dell Server Power Monitor"""

    async def async_step_user(self, user_input=None):
        """First step in the UI"""
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title="Dell Server Power", data=user_input)

        data_schema = vol.Schema({
            vol.Required(CONF_IDRAC_IP): str,
            vol.Required(CONF_IDRAC_USERNAME): str,
            vol.Required(CONF_IDRAC_PASSWORD): str,
            vol.Required(CONF_MQTT_SERVER): str,
            vol.Optional(CONF_MQTT_PORT, default=DEFAULT_MQTT_PORT): int,
            vol.Optional(CONF_MQTT_USERNAME, default=""): str,
            vol.Optional(CONF_MQTT_PASSWORD, default=""): str
        })

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)