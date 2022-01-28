"""Config flow for SENZ WiFi."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from homeassistant.components import persistent_notification
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import config_entry_oauth2_flow

from .const import DOMAIN
from .pysenz import PreAPI


class OAuth2FlowHandler(
    config_entry_oauth2_flow.AbstractOAuth2FlowHandler, domain=DOMAIN
):
    """Config flow to handle SENZ WiFi OAuth2 authentication."""

    DOMAIN = DOMAIN

    @property
    def logger(self) -> logging.Logger:
        """Return logger."""
        return logging.getLogger(__name__)

    @property
    def extra_authorize_data(self) -> dict:
        """Extra data that needs to be appended to the authorize url."""
        return {
            "scope": "restapi offline_access",
        }

    async def async_step_reauth(
        self, entry: dict[str, Any] | None = None
    ) -> FlowResult:
        """Perform reauth upon an API authentication error."""

        self.entry = entry

        persistent_notification.async_create(
            self.hass,
            f"Senz integration for account {entry['auth_implementation']} needs to be re-authenticated. Please go to the [integrations page](/config/integrations) to re-configure it.",
            "Senz re-authentication",
            "senz_reauth",
        )
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Dialog that informs the user that reauth is required."""
        if user_input is None:
            return self.async_show_form(
                step_id="reauth_confirm",
                description_placeholders={"account": self.entry["auth_implementation"]},
                data_schema=vol.Schema({}),
                errors={},
            )

        persistent_notification.async_dismiss(self.hass, "senz_reauth")
        return await self.async_step_user()

    async def async_oauth_create_entry(self, data: dict) -> dict:
        """Create an oauth config entry or update existing entry for reauth."""

        pre_api = PreAPI(self.hass)
        resp = await pre_api.getAccount(data["token"]["access_token"])
        account = resp["userName"];

        existing_entry = await self.async_set_unique_id(account)
        if existing_entry:
            self.hass.config_entries.async_update_entry(existing_entry, data=data)
            await self.hass.config_entries.async_reload(existing_entry.entry_id)
            return self.async_abort(reason="reauth_successful")
        return self.async_create_entry(title=account, data=data)
