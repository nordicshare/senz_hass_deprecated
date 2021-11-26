"""API for SENZ WiFi bound to Home Assistant OAuth."""
import logging

# from asyncio import run_coroutine_threadsafe

from aiohttp import ClientSession
from .const import SENZ_API

# from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_entry_oauth2_flow

# from . pysenz import my_pypi_package
from .pysenz import AbstractAuth

_LOGGER = logging.getLogger(__name__)

# TODO the following two API examples are based on our suggested best practices
# for libraries using OAuth2 with requests or aiohttp. Delete the one you won't use.
# For more info see the docs at https://developers.home-assistant.io/docs/api_lib_auth/#oauth2.


# class ConfigEntryAuth(AbstractAuth):
#     """Provide SENZ WiFi authentication tied to an OAuth2 based config entry."""

#     def __init__(
#         self,
#         hass: HomeAssistant,
#         oauth_session: config_entry_oauth2_flow.OAuth2Session,
#     ) -> None:
#         """Initialize SENZ WiFi Auth."""
#         self.hass = hass
#         self.session = oauth_session
#         super().__init__(self.session.token)
#         _LOGGER.debug("ConfigEntryAuth")

#     def refresh_tokens(self) -> str:
#         """Refresh and return new SENZ WiFi tokens using Home Assistant OAuth2 session."""
#         run_coroutine_threadsafe(
#             self.session.async_ensure_token_valid(), self.hass.loop
#         ).result()

#         return self.session.token["access_token"]


class AsyncConfigEntryAuth(AbstractAuth):
    """Provide SENZ WiFi authentication tied to an OAuth2 based config entry."""

    def __init__(
        self,
        websession: ClientSession,
        oauth_session: config_entry_oauth2_flow.OAuth2Session,
    ) -> None:
        """Initialize SENZ WiFi auth."""
        super().__init__(websession, SENZ_API)
        self._oauth_session = oauth_session
        _LOGGER.debug("AsyncConfigEntryAuth")

    async def async_get_access_token(self) -> str:
        """Return a valid access token."""
        if not self._oauth_session.valid_token:
            await self._oauth_session.async_ensure_token_valid()

        return self._oauth_session.token["access_token"]
