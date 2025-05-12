This is a simple task reminder server implemented using FastAPI and can be deployed to Azure with infrastructrure defined in bicep file.

## How to 

### 1. See live server
https://<deployed-app-url>.azurewebsites.net/docs#/

### 2. Create a task
#### 2.1 Create a user
```
curl -X 'POST' \
  'https://<deployed-app-url>.azurewebsites.net/api/v1/users/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_name": "<user_name>",
  "email": "<user_email@example.com>",
  "password": "<password>"
}'
```

### 2.2 Login to get the access token
```
curl -X 'POST' \
  'https://<deployed-app-url>.azurewebsites.net/token' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=password&username=<user_name>&password=<password>&scope=&client_id=string&client_secret=string'
```



DEV notes

1. init project 
```
poetry init
```

2. install dependencies 
```
poetry add fastapi[standard] uvicorn[standard] sqlmodel python-dotenv
```

3. run the application
```
eval $(poetry env activate)
uvicorn main:app --reload
```

5. run the test
```
poetry run pytest -vvs
```

6. docker
```
# build image
docker build -t task-reminder-server-app . 

# run locally
docker run -p 8000:8000 task-reminder-server-app:latest 

#tag and push to docker hub
docker tag task-reminder-server-app tamlt2704/task-reminder-server-app:latest 

docker push tamlt2704/task-reminder-server-app:latest
```

7. azure
```
#login
az login

#show my subscription list 
az account list --output table

#list all my resource group
az group list --output table 

# create resource group
az group create --name DevResourceGroup --location westeurope

#deployment
az deployment group create --resource-group DevResourceGroup --template-file infra\\main.bicep --parameters appName=ReminderServer dockerImage=tamlt2704/task-reminder-server-app:latest

yeasy/simple-web
```