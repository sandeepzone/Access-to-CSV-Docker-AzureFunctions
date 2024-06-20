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
