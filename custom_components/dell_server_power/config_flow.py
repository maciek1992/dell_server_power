import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CONF_IDRAC_IP, CONF_IDRAC_USERNAME, CONF_IDRAC_PASSWORD

class DellServerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Konfiguracja integracji przez UI."""

    async def async_step_user(self, user_input=None):
        """Pierwszy krok konfiguracji."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(title="Dell Server Power", data=user_input)

        schema = vol.Schema(
            {
                vol.Required(CONF_IDRAC_IP): str,
                vol.Required(CONF_IDRAC_USERNAME): str,
                vol.Required(CONF_IDRAC_PASSWORD): str,
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)