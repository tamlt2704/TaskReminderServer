

poetry init
poetry add fastapi uvicorn[standard]

to active virtualenv
    eval $(poetry env activate)    

start the application
    uvicorn main:app --reload

poetry add sqlmodel