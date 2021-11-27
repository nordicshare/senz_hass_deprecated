"""Platform for climate integration."""
from __future__ import annotations

from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import (
    CURRENT_HVAC_HEAT,
    CURRENT_HVAC_IDLE,
    HVAC_MODE_HEAT,
    SUPPORT_TARGET_TEMPERATURE,
)
from homeassistant.const import TEMP_CELSIUS
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import get_coordinator
from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigType,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator = await get_coordinator(hass)

    async_add_entities(
        SenzClimate(coordinator, idx) for idx, ent in enumerate(coordinator.data)
    )


class SenzClimate(CoordinatorEntity, ClimateEntity):
    """Representation of a Thermostat."""

    def __init__(self, coordinator, idx):
        """Initialize the climate entity."""
        super().__init__(coordinator)
        self._idx = idx
        self._attr_name = self.coordinator.data[self._idx]["name"]
        self._attr_native_unit_of_measurement = TEMP_CELSIUS
        self._attr_unique_id = (
            f"climate-{self.coordinator.data[self._idx]['serialNumber']}"
        )
        self._attr_max_temp = 35
        self._attr_min_temp = 5
        self._attr_target_temperature_high = 35
        self._attr_target_temperature_min = 7
        self._attr_target_temperature_step = 0.5
        self._attr_temperature_unit = TEMP_CELSIUS
        self._attr_precision = 0.1
        self._attr_supported_features = SUPPORT_TARGET_TEMPERATURE
        self._attr_hvac_modes = [HVAC_MODE_HEAT]
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.data[self._idx]["serialNumber"])},
            name=self.coordinator.data[self._idx]["name"],
            manufacturer="nVent",
            model="SENZ WiFi Thermostat",
        )

    @property
    def current_temperature(self):
        """Return the current temperature."""
        return self.coordinator.data[self._idx]["currentTemperature"] / 100

    @property
    def target_temperature(self):
        """Return the target temperature."""
        return self.coordinator.data[self._idx]["setPointTemperature"] / 100

    @property
    def hvac_action(self):
        """Return current hvac action."""
        return (
            CURRENT_HVAC_HEAT
            if self.coordinator.data[self._idx]["isHeating"]
            else CURRENT_HVAC_IDLE
        )

    @property
    def hvac_mode(self):
        """Return the current mode."""
        return HVAC_MODE_HEAT