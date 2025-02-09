import asyncio
import logging
import shutil
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Konfiguracja integracji przy użyciu UI"""

    # Asynchroniczne kopiowanie pliku JS do katalogu www
    js_src = hass.config.path("custom_components/dell_server_power/dell_power_panel.js")
    js_dst = hass.config.path("www/dell_power_panel.js")

    try:
        await hass.async_add_executor_job(shutil.copyfile, js_src, js_dst)
        _LOGGER.info("dell_power_panel.js copied successfully")
    except FileNotFoundError:
        _LOGGER.error("File dell_power_panel.js not found, skipping copy.")
    except Exception as err:
        _LOGGER.error(f"Error copying dell_power_panel.js: {err}")

    # Użycie asynchronicznej metody forward_entry_setups
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True
