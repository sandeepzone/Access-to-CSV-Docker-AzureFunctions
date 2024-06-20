import azure.functions as func
import logging
from azure.storage.blob import BlobServiceClient
import tempfile
import os
import subprocess
import pandas as pd
import io

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

# Connection string to Azure Blob Storage
connection_string = "YOUR_BLOB_STORAGE_CONNECTION_STRING"

def list_blobs_in_container(container_name, connection_string):
    logging.info(f"Listing blobs in container: {container_name}")
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    blobs_list = container_client.list_blobs()
    blob_names = [blob.name for blob in blobs_list]
    logging.info(f"Blobs found: {blob_names}")
    return blob_names

def get_table_names(db_path):
    logging.info("Retrieving table names from Access database.")
    result = subprocess.run(['mdb-tables', '-1', db_path], stdout=subprocess.PIPE)
    table_names = result.stdout.decode('utf-8').splitlines()
    logging.info(f"Table names retrieved: {table_names}")
    return table_names

def save_table_to_csv(db_path, table_name, csv_path):
    logging.info(f"Saving table '{table_name}' to CSV.")
    result = subprocess.run(['mdb-export', db_path, table_name], stdout=subprocess.PIPE)
    csv_data = result.stdout.decode('utf-8')
    df = pd.read_csv(io.StringIO(csv_data))
    df.to_csv(csv_path, index=False)
    logging.info(f"Table '{table_name}' saved to '{csv_path}'.")

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    container_name = req.params.get('container_name')
    output_container_name = req.params.get('output_container_name')

    if not container_name or not output_container_name:
        try:
            req_body = req.get_json()
        except ValueError:
            logging.error("No container_name or output_container_name found in query parameters or request body.")
            return func.HttpResponse(
                "Error: container_name and output_container_name parameters are missing in the query string or request body.",
                status_code=400
            )
        else:
            container_name = req_body.get('container_name')
            output_container_name = req_body.get('output_container_name')

    if container_name and output_container_name:
        logging.info(f"Processing container: {container_name}")
        try:
            blobs_list = list_blobs_in_container(container_name, connection_string)
            blob_service_client = BlobServiceClient.from_connection_string(connection_string)

            for blob_name in blobs_list:
                logging.info(f"Processing blob: {blob_name}")
                blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

                # Stream the blob content
                with tempfile.NamedTemporaryFile(suffix='.accdb', delete=False) as temp_file:
                    temp_file_name = temp_file.name
                    blob_client.download_blob().readinto(temp_file)

                try:
                    table_names = get_table_names(temp_file_name)

                    for table_name in table_names:
                        clean_table_name = table_name.replace(" ", "_").replace("-", "_")
                        clean_blob_name = os.path.splitext(blob_name)[0].replace(" ", "_").replace("-", "_")
                        csv_filename = f"{clean_blob_name}_{clean_table_name}.csv"
                        
                        # Save table to CSV
                        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as csv_file:
                            csv_path = csv_file.name
                            save_table_to_csv(temp_file_name, table_name, csv_path)
                            # Upload CSV to output container
                            output_blob_client = blob_service_client.get_blob_client(container=output_container_name, blob=csv_filename)
                            with open(csv_path, "rb") as data:
                                output_blob_client.upload_blob(data, overwrite=True)

                            logging.info(f"CSV '{csv_filename}' uploaded to container '{output_container_name}'.")

                        # Ensure that the temporary CSV file is deleted
                        os.remove(csv_path)

                finally:
                    # Ensure that the temporary Access database file is deleted
                    os.remove(temp_file_name)

            return func.HttpResponse(
                f"Access files in container '{container_name}' converted to CSVs and saved in container '{output_container_name}'.",
                status_code=200
            )

        except Exception as e:
            logging.error(f"An error occurred while processing container '{container_name}': {e}")
            return func.HttpResponse(
                f"Error processing container '{container_name}': {e}",
                status_code=500
            )

    else:
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass container_name and output_container_name in the query string or in the request body for processing.",
            status_code=200
        )
