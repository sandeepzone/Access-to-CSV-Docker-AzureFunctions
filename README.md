# Azure Functions - Access to CSV Converter

This Azure Functions project provides a serverless HTTP endpoint to convert Microsoft Access (`.accdb`) files stored in an Azure Blob Storage container into CSV files. The converted CSV files are saved in a specified output container.

## Features

- List Access files in a specified Azure Blob Storage container.
- Convert Access tables to CSV format.
- Save CSV files to another Azure Blob Storage container.

## Prerequisites

- **Azure Account**: You need an Azure account to create and manage Azure resources.
- **Azure Blob Storage**: Ensure you have an Azure Blob Storage account with the appropriate containers created.
- **Azure Functions Core Tools**: For local development and testing.

## Installation

1. **Clone the Repository**:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Set Up the Environment**:
    - Ensure you have Python and `pip` installed.
    - Install required Python packages:
      ```bash
      pip install -r requirements.txt
      ```

3. **Azure Functions Core Tools**:
    - Install Azure Functions Core Tools for local development.
      ```bash
      npm install -g azure-functions-core-tools@4 --unsafe-perm true
      ```

## Configuration

1. **Azure Blob Storage Connection String**:
    - Replace `"YOUR_BLOB_STORAGE_CONNECTION_STRING"` in `function_app.py` with your actual Azure Blob Storage connection string.

2. **Environment Variables**:
    - Configure environment variables for Azure Blob Storage connection string in `local.settings.json` for local development:
      ```json
      {
          "IsEncrypted": false,
          "Values": {
              "AzureWebJobsStorage": "YOUR_BLOB_STORAGE_CONNECTION_STRING",
              "FUNCTIONS_WORKER_RUNTIME": "python"
          }
      }
      ```

## Usage

### Local Development

1. **Run the Function App Locally**:
    ```bash
    func start
    ```

2. **Test the Function**:
    - Send an HTTP POST request to `http://localhost:7071/api/http_trigger` with the following JSON body:
      ```json
      {
          "container_name": "input-container",
          "output_container_name": "output-container"
      }
      ```

### Docker

#### Local Development Dockerfile

- Use `Dockerfile.local` for local development, which includes all necessary configurations for running the function app locally.

#### Production Dockerfile

- Use `Dockerfile` for production deployment to Azure. This Dockerfile is optimized for running the function app in the Azure environment.

**Build and Run Locally with Docker**:

1. **Build the Docker Image**:
    ```bash
    docker build -t access-to-csv-converter -f Dockerfile.local .
    ```

2. **Run the Docker Container**:
    ```bash
    docker run -p 7071:80 -e AzureWebJobsStorage="YOUR_BLOB_STORAGE_CONNECTION_STRING" access-to-csv-converter
    ```

## Deployment

1. **Deploy to Azure**:
    ```bash
    func azure functionapp publish <YourFunctionAppName>
    ```

2. **Configure Application Settings**:
    - Set `AzureWebJobsStorage` to your Blob Storage connection string in the Azure Function App's Configuration settings on the Azure portal.

## Endpoints

### HTTP Trigger

- **URL**: `/api/http_trigger`
- **Method**: POST
- **Parameters**:
    - `container_name` (string): The name of the Azure Blob Storage container with Access files.
    - `output_container_name` (string): The name of the Azure Blob Storage container to save CSV files.

**Example Request**:
```bash
curl -X POST "http://<your-function-app-name>.azurewebsites.net/api/http_trigger" \
    -H "Content-Type: application/json" \
    -d '{
        "container_name": "input-container",
        "output_container_name": "output-container"
    }'
