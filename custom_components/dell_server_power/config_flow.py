import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CONF_IDRAC_IP, CONF_IDRAC_USERNAME, CONF_IDRAC_PASSWORD, CONF_MQTT_SERVER, CONF_MQTT_PORT, CONF_MQTT_USERNAME, CONF_MQTT_PASSWORD, CONF_COST_PER_KWH

DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_IDRAC_IP): str,
    vol.Required(CONF_IDRAC_USERNAME): str,
    vol.Required(CONF_IDRAC_PASSWORD): str,
    vol.Required(CONF_MQTT_SERVER): str,
    vol.Optional(CONF_MQTT_PORT, default=1883): int,
    vol.Optional(CONF_MQTT_USERNAME, default=""): str,
    vol.Optional(CONF_MQTT_PASSWORD, default=""): str,
    vol.Optional(CONF_COST_PER_KWH, default=0.75): float  # Domyślna cena za kWh
})

class DellServerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Dell Server Power Monitor."""
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="Dell Server Power", data=user_input)
        return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA)