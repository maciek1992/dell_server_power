import logging
import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CONF_IDRAC_IP, CONF_IDRAC_USERNAME, CONF_IDRAC_PASSWORD, CONF_PRICE_PER_KWH

_LOGGER = logging.getLogger(__name__)

class DellServerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Konfiguracja UI"""

    async def async_step_user(self, user_input=None):
        """Konfiguracja wejścia użytkownika"""
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(
                    {
                        vol.Required(CONF_IDRAC_IP): str,
                        vol.Required(CONF_IDRAC_USERNAME): str,
                        vol.Required(CONF_IDRAC_PASSWORD): str,
                        vol.Optional(CONF_PRICE_PER_KWH, default=0.75): float,
                    }
                ),
            )

        return self.async_create_entry(title="Dell Server Power Monitor", data=user_input)
