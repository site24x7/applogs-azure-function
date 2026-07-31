import azure.functions as func
from shared_code import log_processor


def main(messages: func.ServiceBusMessage):
    log_processor.process_messages(messages)
