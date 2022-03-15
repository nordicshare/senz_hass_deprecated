[![senz_hass](https://img.shields.io/github/v/release/astrandb/senz_hass)](https://github.com/astrandb/senz_hass/releases/latest) [![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs) ![Validate with hassfest](https://github.com/astrandb/senz_hass/workflows/Validate%20with%20hassfest/badge.svg) ![Maintenance](https://img.shields.io/maintenance/yes/2022.svg) [![senz_hass_downloads](https://img.shields.io/github/downloads/astrandb/senz_hass/total)](https://github.com/astrandb/senz_hass) [![senz_hass_downloads](https://img.shields.io/github/downloads/astrandb/senz_hass/latest/total)](https://github.com/astrandb/senz_hass)

# SENZ Wifi Integration for Home Assistant

This integration will represent your SENZ WiFi thermostats as climate entities in Home Assistant. There is also a temperature sensor to simplify use in the UI.

## Installation

Make sure you have the credentials available for your account with nVent cloud.

### Preferred download method

- Use HACS, add this repo as a custom repository and install SENZ WiFi integration.
- Restart Home Assistant

### Manual download method

- Copy all files from custom_components/senz in this repo to your config custom_components/senz
- Restart Home Assistant

### Setup

In Home Assistant 2022.3 or later the client_id/client_secret will be handled by NabuCasa account linking. You will not need your own credentials from the manufacturer and you don't need to enter anything into `configuration.yaml`.

If you are using an older version if Home Assistant you must request a client_id and client_secret from the [manufacturer SENZ/Raychem](https://api.senzthermostat.nvent.com/). Ask for a set of credentials for Home Assistant integration.
Enter following lines to `configuration.yaml`

```yaml
senz:
  client_id: your_client_id
  client_secret: your_client_secret
```

Goto Integrations->Add and select Senz WiFi

Follow instructions to authenticate with nVent cloud server. Allow full access for Home Assistant client.
Clear the browser cache and try again if the Senz Integration does not appear in the list.

## Disclaimer

The package and its author are not affiliated with nVent or Raychem. Use at your own risk.

## License

The package is released under the MIT license.
