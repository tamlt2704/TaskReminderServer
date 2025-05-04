
poetry env use /usr/bin/python3
poetry init
poetry add fastapi uvicorn[standard] sqlmodel

to active virtualenv
    eval $(poetry env activate)    

start the application
    uvicorn main:app --reload

show installed packages
    poetry show 