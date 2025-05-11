import pytest
from sqlmodel import SQLModel, Session, create_engine
import logging
import logging.config

test_engine = create_engine("sqlite:///test.db", connect_args={"check_same_thread": False})
logging.config.fileConfig(fname='log.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

def override_get_session():
    with Session(test_engine) as session:
        yield session
        # session.rollback()
        
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    logger.info('init database')
    SQLModel.metadata.create_all(test_engine)
    yield
    logger.info('cleanup database')
    SQLModel.metadata.drop_all(test_engine)