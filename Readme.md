This is a simple task reminder server implemented using FastAPI and can be deployed to Azure with infrastructrure defined in bicep file.

# How to 

## 1. See live server
https://<deployed-app-url>.azurewebsites.net/docs#/

## 2. Create a task
### 2.1 Create a user
POST /api/v1/users

Example:
```
{
  "user_name": "demo",
  "email": "demo@example.com",
  "password": "admin123"
}
```
### 2.2 Login to get the access token

POST /api/v1/token

using user name and password. Example: demo/admin123

### 2.3 Create a task
POST /api/v1/tasks

## 3. Adjust existing Task Reminder
### 3.1 Get task id 
GET /api/v1/tasks/usertask/{username}

Example: /api/v1/tasks/usertask/demo. This should return tasks assiged to user with id

### 3.2 Updating Task Reminder (login required, see step 2.2)
PUT /api/v1/tasks/{taskid}

Example
```
{
  "reminder_type": "slack" # change reminder type to slack
}
```

## 4. Delete existing Task Reminder
DELETE /api/v1/tasks/{taskid}

## 5. List existing Task Reminders
GET /api/v1/tasks/usertask/{username}

## 6. Show details of a specific Task Reminder
GET /api/v1/tasks/{taskid}


# TODO
* Add more testing 
* Update github workflow to deploy to azure cloud (currently just able to update docker image once pushed to main branch)
* Using proper database (e.g: postgresql) instead of sqlite

----------------------------
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
```