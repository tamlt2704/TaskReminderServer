

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
docker run -p 8000:8000 task-reminder-server-app 

#tag and push to docker hub
docker tag task-reminder-server-app:latest tamlt2704/task-reminder-server-app:latest 

docker push tamlt2704/task-reminder-server-app
```