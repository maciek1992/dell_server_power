import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CONF_IDRAC_IP, CONF_IDRAC_USERNAME, CONF_IDRAC_PASSWORD, CONF_PRICE_PER_KWH

class DellServerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Konfiguracja UI dla integracji Dell Server Power Monitor"""

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="Dell Server Power", data=user_input)

        data_schema = vol.Schema({
            vol.Required(CONF_IDRAC_IP): str,
            vol.Required(CONF_IDRAC_USERNAME): str,
            vol.Required(CONF_IDRAC_PASSWORD): str,
            vol.Required(CONF_PRICE_PER_KWH, default=0.75): vol.Coerce(float),
        })

        return self.async_show_form(step_id="user", data_schema=data_schema)