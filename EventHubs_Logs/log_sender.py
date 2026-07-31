import azure.functions as func
from shared_code import log_processor


def main(eventMessages: func.EventHubEvent):
    log_processor.process_messages(eventMessages)
