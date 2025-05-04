# from typing import Optional
# from fastapi import FastAPI
# from fastapi import Depends, FastAPI, HTTPException, Query
# from sqlmodel import Field, Session, SQLModel, create_engine, select
# from datetime import datetime, timezone
# from sqlmodel import Field, SQLModel, create_engine

# sqlite_file_name = "database.db"
# sqlite_url = f"sqlite:///{sqlite_file_name}"

# engine = create_engine(sqlite_url, echo=True)

# SQLModel.metadata.create_all(engine)


# class BaseEntity(SQLModel):
#     id: int = Field(default=None, primary_key=True)
#     created_at: datetime = Field(
#         default_factory=lambda: datetime.now(timezone.utc)
#     )
#     updated_at: datetime = Field(
#         default_factory=lambda: datetime.now(timezone.utc),
#         sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
#     )

# class Task(BaseEntity, table=True):
#     pass


# # Code below omitted 👇

# app = FastAPI()

# @app.get("/")
# async def main_route():
#     return {"message": "Hello world"}

from taskreminder.app import app
import taskreminder.routes