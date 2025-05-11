

DEV notes

1. init project 
poetry init

2. install dependencies 
poetry add fastapi[standard] uvicorn[standard] sqlmodel python-dotenv

3. dev dependencies
poetry add --group dev pytest httpx

4. run the application
uvicorn main:app --reload