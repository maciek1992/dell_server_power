import logging
import os
import shutil
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Inicjalizacja wtyczki Dell Server Power Monitor"""
    hass.async_create_task(hass.config_entries.async_forward_entry_setups(entry, ["sensor"]))

    # 📌 Ścieżka do pliku UI panelu
    js_src = os.path.join(os.path.dirname(__file__), "dell_power_panel.js")
    js_dst = hass.config.path("www/dell_power_panel.js")

    # 📌 Kopiowanie pliku panelu do katalogu /www/
    if not os.path.exists(js_dst):
        try:
            shutil.copyfile(js_src, js_dst)
            _LOGGER.info("Plik UI dell_power_panel.js skopiowany do katalogu www/")
        except Exception as e:
            _LOGGER.error(f"Błąd kopiowania dell_power_panel.js: {e}")

    # 📌 Dodanie zakładki do panelu bocznego Home Assistant
    yaml_path = hass.config.path("configuration.yaml")
    try:
        with open(yaml_path, "r+") as f:
            content = f.read()
            if "panel_custom:" not in content:
                f.write("\npanel_custom:\n")
            if "dell_server_power" not in content:
                f.write("  - name: 'dell_server_power'\n")
                f.write("    sidebar_title: 'Zużycie Serwera'\n")
                f.write("    sidebar_icon: 'mdi:server'\n")
                f.write("    module_url: '/local/dell_power_panel.js'\n")
                f.write("    require_admin: false\n")
        _LOGGER.info("Zakładka 'Zużycie Serwera' dodana do menu Home Assistant.")
    except Exception as e:
        _LOGGER.error(f"Błąd modyfikacji configuration.yaml: {e}")

    return True