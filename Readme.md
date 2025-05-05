
poetry env use /usr/bin/python3
poetry init
poetry add fastapi uvicorn[standard] sqlmodel pytest

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


az group create -n taskReminder -l westus
