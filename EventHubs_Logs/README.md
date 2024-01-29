# Forwards logs from Azure Eventhub

You can configure an automated deployment by following the steps mentioned in this [document](https://www.site24x7.com/help/log-management/).

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fsite24x7%2Fapplogs-azure-function%2Fmaster%2Fdeployment%2Fsite24x7-azure-deployment.json)

| Function | Description |
|---|---|
| Subscription | Choose your subscription mode. |
| Resource group | Create a new resource group with a name similar to Site24x7-Azure-Logs. | 
| Location | Choose a location. |
| Name | The function name will be prefilled. You don’t need to change it. |
| Log Type Config | Navigate to the Site24x7 web client, select **Admin > Applogs > Log Profile**, then select the created log profile, and copy the code that appears on the screen as the input for the variable logtypeConfig. |

### Architecture 

![Architecture](Images/EventHubs_Logs/Architecture.png)