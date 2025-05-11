

DEV notes

1. init project 
poetry init

2. install dependencies 
poetry add fastapi[standard] uvicorn[standard] sqlmodel python-dotenv

3. run the application
eval $(poetry env activate)
uvicorn main:app --reload

5. run the test
poetry run pytest -s # -s for printing