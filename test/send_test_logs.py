"""Test sender: pushes sample JSON log messages to a Service Bus queue.

Usage:
  pip install azure-servicebus
  export SB_CONNECTION_STRING="Endpoint=sb://..."
  export SB_QUEUE_NAME="site24x7-test-logs"
  python send_test_logs.py [count]

Sends three payload shapes the Site24x7 function supports:
  1. Azure diagnostic format: {"records": [...]}
  2. JSON array of events
  3. Single JSON event
"""
import json
import os
import sys
from datetime import datetime, timezone

from azure.servicebus import ServiceBusClient, ServiceBusMessage

CONN = os.environ["SB_CONNECTION_STRING"]
QUEUE = os.environ["SB_QUEUE_NAME"]
COUNT = int(sys.argv[1]) if len(sys.argv) > 1 else 5


def make_event(i):
    return {
        "time": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f"),
        "level": "Informational" if i % 3 else "Error",
        "operationName": "TestApp/WriteLog",
        "category": "TestAppLogs",
        "message": f"test log event {i} from send_test_logs.py",
    }


def main():
    with ServiceBusClient.from_connection_string(CONN) as client:
        with client.get_queue_sender(QUEUE) as sender:
            # 1. diagnostic-style records batch
            sender.send_messages(ServiceBusMessage(
                json.dumps({"records": [make_event(i) for i in range(COUNT)]})))
            # 2. bare array
            sender.send_messages(ServiceBusMessage(
                json.dumps([make_event(100 + i) for i in range(2)])))
            # 3. single event
            sender.send_messages(ServiceBusMessage(json.dumps(make_event(999))))
    print(f"sent {COUNT} + 2 + 1 events to queue '{QUEUE}'")


if __name__ == "__main__":
    main()
