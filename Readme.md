
poetry env use /usr/bin/python3
poetry init
poetry add fastapi[standard] uvicorn[standard] sqlmodel pytest
#authentication
poetry add pyjwt passlib[bcrypt]

to active virtualenv
    eval $(poetry env activate)    

start the application
    uvicorn main:app --reload

show installed packages
    poetry show 

run pytests
    poetry run pytest -s


# Login and create resource group
az login
az group create --name my-fastapi-rg --location eastus

# Deploy Bicep
az deployment group create \
  --resource-group my-fastapi-rg \
  --template-file bicep/main.bicep \
  --parameters postgresAdminUsername=admin postgresAdminPassword=MySecretPwd123

install az within wsl
    curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

login
    az login

show my subscription list 
    az account list --output table

change subcription
    az account set --subscription <subscription id>

az group list --output table
    list all my resource group

create resource group
    az group create --name DevResourceGroup --location westeurope

list all resource group
    az group list --output table

delete resource group
    az group delete --name TaskReminderServerGroup --yes

deploy web app
    az deployment group create \
    --resource-group DevResourceGroup \
    --template-file bicep\\main.bicep \
    --parameters webAppName=TaskReminderServer

docker build -t task-reminder-server-app .
docker run -p 8000:8000 task-reminder-server-app
docker tag task-reminder-server-app:latest tamlt2704/task-reminder-server-app:latest
docker push tamlt2704/task-reminder-server-app