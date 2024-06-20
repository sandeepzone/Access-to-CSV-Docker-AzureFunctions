FROM mcr.microsoft.com/azure-functions/python:4-python3.10
 
ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
   AzureFunctionsJobHost__Logging__Console__IsEnabled=true
 
# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    mdbtools \
    unixodbc-dev \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Azure Functions Core Tools
RUN apt-get update && apt-get install -y \
    apt-transport-https \
    && curl -sL https://deb.nodesource.com/setup_14.x | bash - \
    && curl -sL https://aka.ms/InstallAzureCLIDeb | bash \
    && apt-get install -y azure-functions-core-tools-4
    

# Install Python packages
COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

# Copy the function app code
COPY . /home/site/wwwroot
