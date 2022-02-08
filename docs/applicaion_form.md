## Example of application for client_id and client_secret

| Field name                | Field                                                                                                      | Comments                                                                                                      |
| ------------------------- | ---------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| Definition of project     | Integrate SENZ thermostats with Home Assistant.                                                            |
| Grant types/flows         | Authorization code                                                                                         |
| Offline access            | Yes                                                                                                        |
| Client ID                 | \<YourName\>\_HomeAssistant                                                                                |
| Redirect URIs             | http://localhost:8123/auth/external/callback, http://homeassistant.local:8123/auth/external/callback       | Add the url you normally use to access your Homeassistant installation on your local LAN and/or from Internet |
| Post logout redirect URIs | \<none\>                                                                                                   |                                                                                                               |
| Allowed CORS origins      | \<none\>                                                                                                   |                                                                                                               |
| Company Name              |                                                                                                            |
| Contact Name              |                                                                                                            | Uour name                                                                                                     |
| Contact Info              |                                                                                                            | Your email                                                                                                    |
| Access to SENZ WIFI       | By signing in, you are authorizing your Home Assistant instance to access your devices                     |
| Description               | Home Assistant will monitor measured temperature and manage set-point and mode from GUI and/or automations |                                                                                                               |
| Permission                | By signing in , you are authorizing your Home Assistant instance to access your thermostats                |                                                                                                               |
