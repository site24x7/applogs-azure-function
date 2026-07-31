import re

class BlobDetails:
    def __init__(self, blob_path):
        self.vNet = False
        if blob_path:
            if "flowLogResourceID=" in blob_path:
                self.vNet = True
                pattern = re.compile(".*flowLogResourceID=/(?P<subId>[^/_]+)_(?P<resourceGroup>[^/]+)/(?P<serviceGroup>\w+)_(?P<Location>\w+)_(?P<flowLogName>[^/]+)/y=(?P<blobYear>[^/]+)/m=(?P<blobMonth>[^/]+)/d=(?P<blobDay>[^/]+)/h=(?P<blobHour>[^/]+)/m=(?P<blobMinute>[^/]+)(?:/macAddress=(?P<mac>[^/]+))?.*")
            else:
                pattern = re.compile(".*SUBSCRIPTIONS/(?P<subId>[^/]+)/RESOURCEGROUPS/(?P<resourceGroup>[^/]+)/PROVIDERS/(?P<resourceNamespace>[^/]+)/(?P<serviceGroup>[^/]+)/(?P<serviceName>[^/]+)/y=(?P<blobYear>[^/]+)/m=(?P<blobMonth>[^/]+)/d=(?P<blobDay>[^/]+)/h=(?P<blobHour>[^/]+)/m=(?P<blobMinute>[^/]+)(?:/macAddress=(?P<mac>[^/]+))?.*")
            match = pattern.match(blob_path)
            if match:
                self.subscription_id = match.group("subId")
                self.resource_group = match.group("resourceGroup")
                self.service_group = match.group("serviceGroup")
                self.year = match.group("blobYear")
                self.month = match.group("blobMonth")
                self.day = match.group("blobDay")
                self.hour = match.group("blobHour")
                self.minute = match.group("blobMinute")
                if match.group("mac") != None:
                    self.mac = match.group("mac")
                if self.vNet:
                    self.Location = match.group("Location")
                    self.flowLogName = match.group("flowLogName")
                else:
                    self.resource_namespace = match.group("resourceNamespace")
                    self.service_name = match.group("serviceName")



    def get_partition_key(self):
        if self.vNet:
            return f"{self.subscription_id.replace('-', '_')}_{self.resource_group}_{self.flowLogName}_{self.mac}"
        elif hasattr(self,"mac"):
            return f"{self.subscription_id.replace('-', '_')}_{self.resource_group}_{self.service_name}_{self.mac}"
        else:
            return f"{self.subscription_id.replace('-', '_')}_{self.resource_group}_{self.service_name}"
    def get_row_key(self):
        return f"{self.year}_{self.month}_{self.day}_{self.hour}_{self.minute}"

    def __str__(self):
        if self.vNet:
            return f"{self.resource_group}_{self.flowLogName}_{self.day}_{self.hour}"
        return f"{self.resource_group}_{self.service_name}_{self.day}_{self.hour}"
