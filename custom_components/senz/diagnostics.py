"""Diagnostics support for Senz."""
from __future__ import annotations

from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntry
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN

TO_REDACT = {
    # CONF_PASSWORD,
    # CONF_USERNAME,
    "access_token",
    "refresh_token",
}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, config_entry: ConfigEntry
) -> dict:
    """Return diagnostics for a config entry."""
    coordinator: DataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id][
        "coordinator"
    ]

    diagnostics_data = {
        "info": async_redact_data(config_entry.data, TO_REDACT),
        "api_data": async_redact_data(coordinator.data, TO_REDACT),
    }

    return diagnostics_data


async def async_get_device_diagnostics(
    hass: HomeAssistant, config_entry: ConfigEntry, device: DeviceEntry
) -> dict[str, Any]:
    """Return diagnostics for a device."""
    info = {}
    info["manufacturer"] = device.manufacturer
    info["model"] = device.model

    coordinator: DataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id][
        "coordinator"
    ]

    device_data = coordinator.data
    diagnostics_data = {
        "info": async_redact_data(info, TO_REDACT),
        "api_data": async_redact_data(device_data, TO_REDACT),
    }

    return diagnostics_data
