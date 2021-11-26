"""Platform for sensor integration."""
from __future__ import annotations

from homeassistant.components.sensor import STATE_CLASS_MEASUREMENT, SensorEntity, DEVICE_CLASS_TEMPERATURE
from homeassistant.const import TEMP_CELSIUS
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from . import get_coordinator

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities,
) -> None:
    """Set up the sensor platform."""
    coordinator = await get_coordinator(hass)

    async_add_entities(SenzSensor(coordinator, idx) for idx, ent in enumerate(coordinator.data)
)


class SenzSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, coordinator, idx):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._idx = idx
        self._state = None
        self._attr_name = self.coordinator.data[self._idx]["name"]
        self._attr_device_class = DEVICE_CLASS_TEMPERATURE
        self._attr_native_unit_of_measurement = TEMP_CELSIUS
        self._attr_state_class = STATE_CLASS_MEASUREMENT
        self._attr_unique_id = f"temp-{self.coordinator.data[self._idx]['serialNumber']}"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.coordinator.data[self._idx]["currentTemperature"] / 100

