# Site24x7 Event Hub Function

Collects Azure diagnostics logs streamed to an Event Hub and forwards them to Site24x7 AppLogs.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fsite24x7%2Fapplogs-azure-function%2Fmaster%2Fdeployment%2Fsite24x7-azure-deployment.json)

The deployment creates an Event Hub namespace with the event hub `Site24x7-Operational-Logs`, a Basic (B1) Linux App Service plan, a storage account, and the function app. Configure your Azure resources' diagnostic settings to stream logs to this event hub.

## Input parameters

| Parameter | Required | Default | Description |
|---|---|---|---|
| Subscription | Yes | — | The Azure subscription to deploy into. |
| Resource group | Yes | — | Create a new resource group (e.g. `Site24x7-Azure-Logs`). |
| Region | Yes | — | Azure region for all created resources. |
| Name | Yes | `Site24x7AzureLogs` | Prefix used for the function app, App Service plan, Event Hub namespace, and storage account names. |
| Log Type Config | Yes | — | Base64 configuration string from the Site24x7 web client: **Admin > AppLogs > Log Profile**, open the profile and copy the code shown. Stored in the `logTypeConfig` app setting. |
| Debug Mode | No | `False` | Set `True` to print the first event of each batch to the function logs for troubleshooting. |

## How it works

- Events are consumed in batches from the event hub (`$Default` consumer group).
- Each event payload is expected in the Azure diagnostic format `{"records": [...]}`; bare JSON arrays and single JSON objects are also supported.
- The log type config is resolved per event category: an app setting named `S247_<category>` takes precedence, otherwise `logTypeConfig` is used. The optional `Identifier` app setting can name a field to resolve the category from instead.
- Parsed events are batched, gzip-compressed, and uploaded to the Site24x7 AppLogs endpoint from the config.
