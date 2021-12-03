"""Platform for climate integration."""
from __future__ import annotations

from typing import Any

from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import (
    CURRENT_HVAC_HEAT,
    CURRENT_HVAC_IDLE,
    HVAC_MODE_AUTO,
    HVAC_MODE_HEAT,
    HVAC_MODE_OFF,
    SUPPORT_TARGET_TEMPERATURE,
)
from homeassistant.const import ATTR_TEMPERATURE, TEMP_CELSIUS
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
    coordinator = await get_coordinator(hass, config_entry)

    async_add_entities(
        SenzClimate(coordinator, idx, hass, config_entry)
        for idx, ent in enumerate(coordinator.data)
    )


class SenzClimate(CoordinatorEntity, ClimateEntity):
    """Representation of a Thermostat."""

    def __init__(self, coordinator, idx, hass, entry):
        """Initialize the climate entity."""
        super().__init__(coordinator)
        self._idx = idx
        self._api = hass.data[DOMAIN][entry.entry_id]["api"]
        self._attr_name = self.coordinator.data[self._idx]["name"]
        self._attr_native_unit_of_measurement = TEMP_CELSIUS
        self._attr_unique_id = (
            f"climate-{self.coordinator.data[self._idx]['serialNumber']}"
        )
        self._attr_max_temp = 35
        self._attr_min_temp = 5
        self._attr_target_temperature_high = 35
        self._attr_target_temperature_min = 5
        self._attr_target_temperature_step = 0.5
        self._attr_temperature_unit = TEMP_CELSIUS
        self._attr_precision = 0.1
        self._attr_supported_features = SUPPORT_TARGET_TEMPERATURE
        self._attr_hvac_modes = [HVAC_MODE_HEAT, HVAC_MODE_OFF, HVAC_MODE_AUTO]
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.data[self._idx]["serialNumber"])},
            name=self.coordinator.data[self._idx]["name"],
            manufacturer="nVent",
            model="SENZ WiFi Thermostat",
        )

    @property
    def current_temperature(self):
        """Return the current temperature."""
        return round(self.coordinator.data[self._idx]["currentTemperature"] / 100, 1)

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
        """ Since API does not support off mode we simulate it by manual mode and 5C."""
        mode = self.coordinator.data[self._idx]["mode"]
        if mode == 5 or (
            mode == 3 and self.coordinator.data[self._idx]["setPointTemperature"] == 500
        ):
            return HVAC_MODE_OFF
        if mode == 3:
            return HVAC_MODE_HEAT
        if mode == 1:
            return HVAC_MODE_AUTO
        return

    async def async_set_hvac_mode(self, hvac_mode: str) -> None:
        """Set new hvac mode."""
        if hvac_mode == HVAC_MODE_HEAT:
            await self._api.set_mode_manual(
                self.coordinator.data[self._idx]["serialNumber"]
            )
        elif hvac_mode == HVAC_MODE_AUTO:
            await self._api.set_mode_auto(
                self.coordinator.data[self._idx]["serialNumber"]
            )
        elif hvac_mode == HVAC_MODE_OFF:
            await self._api.set_mode_off(
                self.coordinator.data[self._idx]["serialNumber"]
            )
        await self.coordinator.async_request_refresh()

    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set new target temperature."""
        if (temperature := kwargs.get(ATTR_TEMPERATURE)) is None:
            return
        await self._api.set_target_temperature(
            self.coordinator.data[self._idx]["serialNumber"], int(temperature * 100)
        )
        await self.coordinator.async_request_refresh()
