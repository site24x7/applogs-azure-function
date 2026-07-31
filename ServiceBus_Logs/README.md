# Site24x7 Service Bus Function

Collects JSON log messages from an Azure Service Bus queue and forwards them to Site24x7 AppLogs.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fsite24x7%2Fapplogs-azure-function%2Fmaster%2Fdeployment%2Fsite24x7-azure-servicebus-logs-deployment.json)

The deployment creates a Basic (B1) Linux App Service plan, a storage account, and the function app. It connects to **your existing Service Bus namespace and queue** — both are supplied as parameters.

## Input parameters

| Parameter | Required | Default | Description |
|---|---|---|---|
| Subscription | Yes | — | The Azure subscription to deploy into. |
| Resource group | Yes | — | Create a new resource group (e.g. `Site24x7-Azure-SB-Logs`). |
| Region | Yes | — | Azure region for all created resources. |
| Name | Yes | `Site24x7AzureSBLogs` | Prefix used for the function app, App Service plan, and storage account names. |
| Log Type Config | Yes | — | Base64 configuration string from the Site24x7 web client: **Admin > AppLogs > Log Profile**, open the profile and copy the code shown. Stored in the `logTypeConfig` app setting. |
| Service Bus Connection String | Yes | — | Connection string of your Service Bus namespace with at least **Listen** rights. In the Azure portal: Service Bus Namespace > **Settings > Shared access policies** > select a policy (e.g. `RootManageSharedAccessKey`, or create a Listen-only policy) > copy **Primary connection string**. Stored in the `AzureServiceBusConnectionString` app setting. |
| Service Bus Queue Name | Yes | — | Name of the queue in that namespace to collect logs from. Stored in the `ServiceBusQueueName` app setting. |
| Debug Mode | No | `False` | Set `True` to print the first event of each batch to the function logs for troubleshooting. |

## Supported message formats

Messages sent to the queue must be JSON in one of these shapes:

- Azure diagnostic log format: `{"records": [ {...}, {...} ]}`
- A JSON array of log events: `[ {...}, {...} ]`
- A single JSON log event: `{...}`

## Changing the queue later

Update the `ServiceBusQueueName` and/or `AzureServiceBusConnectionString` app settings on the function app — no code change or redeployment needed.

## Using a topic subscription instead of a queue

Replace `queueName` in [function.json](function.json) with:

```json
"topicName": "<your-topic>",
"subscriptionName": "<your-subscription>"
```

## Sending test messages

Use [test/send_test_logs.py](../test/send_test_logs.py) to push sample events in all supported formats to a queue, or use **Service Bus Explorer** in the Azure portal (queue > Service Bus Explorer > Send messages).
