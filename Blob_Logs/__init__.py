import logging,os
import azure.functions as func
from azure.storage.blob import BlobServiceClient
from azure.data.tables import TableServiceClient
from Blob_Logs import blob_details,check_point
from shared_code import log_processor
from datetime import datetime
import ast

blob_connection_string = os.environ["blobconnectionstring"]
table_connection_string = os.environ["AzureWebJobsStorage"]
timestamp = os.environ["LogCollectionStartTime"]
tail = ast.literal_eval(os.environ["Tail"])

global initialized
initialized = False

if not initialized:
    with TableServiceClient.from_connection_string(table_connection_string) as table_service_client:
        table_service_client.create_table_if_not_exists(table_name="Checkpoints")
    initialized = True

def main(myblob: func.InputStream):
    try:
        logging.info(f"Python blob trigger function processed blob Name: {myblob.name}")
        current_time_str = myblob.blob_properties["LastModified"]
        current_time = datetime.fromisoformat(current_time_str).timestamp()
        if int(current_time) < int(timestamp):
            return
        azure_logger = logging.getLogger("azure.core.pipeline.policies.http_logging_policy")
        azure_logger.setLevel(logging.WARNING)
        container_name, blob_name = myblob.name.split('/', 1)
        if tail:
            blobDetails = blob_details.BlobDetails(str(myblob.name))
            serviceName = blobDetails.service_group
            check_pointDB = check_point.check_point(table_connection_string)
            checkpoint = check_pointDB.get_check_point(blobDetails)
        
        blob_service_client = BlobServiceClient.from_connection_string(blob_connection_string)
        blob_client = blob_service_client.get_blob_client(container=container_name,blob=blob_name)
        block_list = blob_client.get_block_list()
        
        if tail:
            starting_byte = sum(item['size'] for index, item in enumerate(block_list[0]) if index < checkpoint['check_pointIndex'])
            ending_byte = sum(item['size'] for index, item in enumerate(block_list[0]) if index < len(block_list[0]) - 1)
            data_length = ending_byte - starting_byte
            logging.info(f"Blob: {blobDetails}, starting byte: {starting_byte}, ending byte: {ending_byte}, number of bytes: {data_length}")
            blob_data=blob_client.download_blob(offset=(starting_byte),length=data_length)
        else:
            blob_data=blob_client.download_blob()
            serviceName=None
        try:
            blob_content = blob_data.readall()
            if blob_content and blob_content[0] == 0x2C:
                blob_content = blob_content[1:]
            log_processor.process_blob_data(blob_content,container_name,serviceName)
            if tail:
                checkpoint['check_pointIndex'] = (len(block_list[0])-1)
                check_pointDB.put_check_point(checkpoint)
            return
        except Exception:
            logging.exception("Blob processing failed")
            return
    except Exception:
        logging.exception("Blob trigger failed")