# import blob_Sender
from datetime import datetime
import logging,traceback

field_mapping = {
        "Time" : 0,
        "SourceIP": 1,
        "DestinationIP": 2,
        "SourcePort": 3,
        "DestinationPort": 4,
        "Protocol": 5,
        "FlowDirection": 6,
        "FlowState": 7,
        "FlowEncryption": 8,
        "PacketsSent": 9,
        "BytesSent": 10,
        "PacketsReceived": 11,
        "BytesReceived": 12,
    }
    
trafficAction_mapping = {
    "B": "Begin",
    "C": "Continuing",
    "E": "End",
    "D": "Denied"
}   

def processData(dataList,log_line_filter):
    parsed_lines = []
    log_size = 0
    try:
        metadata = {
            "FlowLogVersion": dataList["flowLogVersion"],
            "FlowLogGUID": dataList["flowLogGUID"],
            "MacAddress": dataList["macAddress"],
            "ResourceCategory": dataList["category"],
            "FlowLogResourceID": dataList["flowLogResourceID"],
            "TargetResourceID": dataList["targetResourceID"],
            "OperationName": dataList["operationName"],
        }
        for aclid in dataList["flowRecords"]["flows"]:
            metadata["aclID"] = aclid["aclID"]
            for rule in aclid["flowGroups"]:
                metadata["flowGroups"] = rule["rule"] 
                for flow_tuple in rule["flowTuples"]:
                    data = flow_tuple.split(',')
                    formatted_line = {field: data[index] for field, index in field_mapping.items()}
                    datetime_obj = datetime.utcfromtimestamp(int(int(formatted_line['Time'])/1000))
                    formatted_line['Time'] = datetime_obj.strftime('%Y-%m-%d %H:%M:%S.') + str(int(formatted_line['Time']) % 1000).zfill(3)
                    formatted_line["FlowDirection"] = "Inbound" if formatted_line["FlowDirection"] == "I" else "Outbound"
                    formatted_line["Protocol"] = "TCP" if formatted_line["Protocol"] == "T" else "UDP"
                    formatted_line["FlowState"] = trafficAction_mapping[formatted_line["FlowState"]]
                    formatted_line.update(metadata)
                    parsed_line, size = log_line_filter(formatted_line)
                    if parsed_line:
                        parsed_lines.append(parsed_line)
                        log_size += size
        return parsed_lines,log_size

    except Exception as e:
        traceback.print_exc()