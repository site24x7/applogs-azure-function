# AppLogs-Azure-Function
This repository has Site24x7 Azure functions for collecting logs from Microsoft Azure Blob Storage and Event Hubs, along with Azure ARM templates for automated deployment.

| Function | Description | Deployment |
|---|---|---|
| [Site24x7 Event Hub Function](EventHubs_Logs) | Collects and forwards Azure diagnostics logs from Event Hub to Site24x7 AppLogs. | [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fsite24x7%2Fapplogs-azure-function%2Fmaster%2Fdeployment%2Fsite24x7-azure-deployment.json) |
| [Site24x7 Azure logs Function](NsgFlow_Logs) | Collects and forwards Azure NSG Flow logs from Azure Blob Storage to Site24x7 AppLogs. | [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fsite24x7%2Fapplogs-azure-function%2Fmaster%2Fdeployment%2Fsite24x7-azure-nsgflow-logs-deployment.json) |# AppLogs-Azure-Function
This repository contains a collection of Azure functions to collect data and send to Site24x7 AppLogs
