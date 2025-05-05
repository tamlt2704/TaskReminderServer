from sqlmodel import create_engine

#data source 
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)

# PostgreSQL data source
# postgresql_url = "postgresql://username:password@localhost/dbname"
# postgresql_engine = create_engine(postgresql_url, echo=True)