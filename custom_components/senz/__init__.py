"""The SENZ WiFi integration."""
from __future__ import annotations

import logging
from datetime import timedelta
from http import HTTPStatus

import async_timeout
import voluptuous as vol
from aiohttp.client_exceptions import ClientResponseError
from homeassistant.components.cloud import account_link
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_CLIENT_ID, CONF_CLIENT_SECRET
from homeassistant.core import HomeAssistant
from homeassistant.helpers import aiohttp_client, config_entry_oauth2_flow
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.config_entry_oauth2_flow import LocalOAuth2Implementation
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.update_coordinator import (
    ConfigEntryAuthFailed,
    ConfigEntryNotReady,
    DataUpdateCoordinator,
)

from . import config_flow
from .api import AsyncConfigEntryAuth
from .const import DOMAIN, OAUTH2_AUTHORIZE, OAUTH2_TOKEN

account_link.HA_VERSION = "2022.3.0"

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_CLIENT_ID): cv.string,
                vol.Required(CONF_CLIENT_SECRET): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

PLATFORMS = ["binary_sensor", "climate", "sensor"]


class SenzLocalOAuth2Implementation(LocalOAuth2Implementation):
    def __init__(
        self,
        hass: HomeAssistant,
        domain: str,
        client_id: str,
        client_secret: str,
        authorize_url: str,
        token_url: str,
        name: str,
    ) -> None:
        super().__init__(
            hass, domain, client_id, client_secret, authorize_url, token_url
        )
        self._name = name

    @property
    def name(self) -> str:
        """Name of the implementation"""
        return self._name


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the SENZ WiFi component."""
    hass.data[DOMAIN] = {}

    if DOMAIN not in config:
        return True

    config_flow.OAuth2FlowHandler.async_register_implementation(
        hass,
        # config_entry_oauth2_flow.LocalOAuth2Implementation(
        SenzLocalOAuth2Implementation(
            hass,
            DOMAIN,
            config[DOMAIN][CONF_CLIENT_ID],
            config[DOMAIN][CONF_CLIENT_SECRET],
            OAUTH2_AUTHORIZE,
            OAUTH2_TOKEN,
            "nVent/SENZ",
        ),
    )

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up SENZ WiFi from a config entry."""
    implementation = (
        await config_entry_oauth2_flow.async_get_config_entry_implementation(
            hass, entry
        )
    )

    session = config_entry_oauth2_flow.OAuth2Session(hass, entry, implementation)
    try:
        await session.async_ensure_token_valid()
    except ClientResponseError as ex:
        _LOGGER.debug("API error: %s (%s)", ex.code, ex.message)
        if ex.code in (
            HTTPStatus.BAD_REQUEST,
            HTTPStatus.UNAUTHORIZED,
            HTTPStatus.FORBIDDEN,
        ):
            raise ConfigEntryAuthFailed("Token not valid, trigger renewal") from ex
        raise ConfigEntryNotReady from ex

    hass.data[DOMAIN][entry.entry_id] = {}
    hass.data[DOMAIN][entry.entry_id]["api"] = AsyncConfigEntryAuth(
        aiohttp_client.async_get_clientsession(hass), session
    )

    coordinator = await get_coordinator(hass, entry)
    if not coordinator.last_update_success:
        await coordinator.async_config_entry_first_refresh()
    # _LOGGER.debug("First data: %s", coordinator.data)

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok


async def get_coordinator(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> DataUpdateCoordinator:
    """Get the data update coordinator."""
    if "coordinator" in hass.data[DOMAIN][entry.entry_id]:
        return hass.data[DOMAIN][entry.entry_id]["coordinator"]

    async def async_fetch():
        senz_api = hass.data[DOMAIN][entry.entry_id]["api"]
        try:
            async with async_timeout.timeout(10):
                res = await senz_api.request("GET", "/Thermostat")
                # _LOGGER.debug("Data: %s", await res.json())
            return await res.json()
        except ClientResponseError as exc:
            if exc.status == 401:
                raise ConfigEntryAuthFailed from exc
            _LOGGER.warning("API fetch failed. Status: %s, - %s", exc.code, exc.message)

    hass.data[DOMAIN][entry.entry_id]["coordinator"] = DataUpdateCoordinator(
        hass,
        logging.getLogger(__name__),
        name=DOMAIN,
        update_method=async_fetch,
        update_interval=timedelta(seconds=30),
    )
    await hass.data[DOMAIN][entry.entry_id]["coordinator"].async_refresh()
    return hass.data[DOMAIN][entry.entry_id]["coordinator"]
