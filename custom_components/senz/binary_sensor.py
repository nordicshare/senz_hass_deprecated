"""Platform for sensor integration."""
from __future__ import annotations

from homeassistant.components.binary_sensor import (
    DEVICE_CLASS_CONNECTIVITY,
    BinarySensorEntity,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo, EntityCategory
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
        SenzBinarySensor(coordinator, idx) for idx, ent in enumerate(coordinator.data)
    )


class SenzBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a Sensor."""

    def __init__(self, coordinator, idx):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._idx = idx
        self._attr_name = self.coordinator.data[self._idx]["name"]
        self._attr_device_class = DEVICE_CLASS_CONNECTIVITY
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_unique_id = (
            f"online-{self.coordinator.data[self._idx]['serialNumber']}"
        )
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.data[self._idx]["serialNumber"])},
            name=self.coordinator.data[self._idx]["name"],
            manufacturer="nVent",
            model="SENZ WiFi Thermostat",
        )

    @property
    def is_on(self):
        """Return the state of the sensor."""
        return self.coordinator.data[self._idx]["online"]
