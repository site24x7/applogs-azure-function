# Site24x7 Storage Blob Function

Collects Azure logs written to a Blob Storage container and forwards them to Site24x7 AppLogs. Supports Azure diagnostic log blobs, **VNET flow logs**, **NSG flow logs**, and plain line-based log files.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fsite24x7%2Fapplogs-azure-function%2Fmaster%2Fdeployment%2Fsite24x7-azure-blob-logs-deployment.json)

The deployment creates a Basic (B1) Linux App Service plan, a storage account for the function's own state, and the function app. It reads from **your existing storage account** where the logs are written — supplied as a parameter.

## Input parameters

| Parameter | Required | Default | Description |
|---|---|---|---|
| Subscription | Yes | — | The Azure subscription to deploy into. |
| Resource group | Yes | — | Create a new resource group (e.g. `Site24x7-Azure-Blob-Logs`). |
| Region | Yes | — | Azure region for all created resources. |
| Name | Yes | `Site24x7BlobLogs` | Prefix used for the function app, App Service plan, and storage account names. |
| blobconnectionstring | Yes | — | Connection string of the storage account that receives the logs. In the Azure portal: Storage account > **Security + networking > Access keys** > copy a **Connection string**. |
| Log Type Config | Yes | — | Base64 configuration string from the Site24x7 web client: **Admin > AppLogs > Log Profile**, open the profile and copy the code shown. Stored in the `logTypeConfig` app setting. |
| Log Collection Start Time | Yes | — | Epoch seconds. Blobs last modified before this time are skipped; use the current epoch time to collect only new logs. |
| Tail | Yes | `True` | `True` for hourly append blobs (NSG / VNET flow logs `PT1H.json`): the function checkpoints processed blocks in a table named `Checkpoints` and reads only new data on each trigger. `False` to read each blob in full as line-based JSON logs. |
| Container Name | Yes | — | Blob container to watch. VNET flow logs: `insights-logs-flowlogflowevent`. NSG flow logs: `insights-logs-networksecuritygroupflowevent`. Any container for plain log files. |

## Supported log sources

- **VNET flow logs** (`FlowLogFlowEvent`): flow tuples parsed via `shared_code/vnet_parser.py`. Enable via Network Watcher > Flow logs targeting a virtual network, subnet, or NIC.
- **NSG flow logs** (`NetworkSecurityGroupFlowEvent`): parsed via `shared_code/nsg_parser.py`. Note: Azure retired new NSG flow log creation on June 30, 2025 — use VNET flow logs for new setups.
- **Azure diagnostic blobs**: records parsed with the `jsonPath` of the log profile; config resolved from the `S247_<SERVICEGROUP>` app setting, falling back to `logTypeConfig`.
- **Plain log files**: with `Tail=False`, each line is parsed as a JSON event; the container name is used as the category.
