from fastapi import FastAPI
import logging
from contextlib import asynccontextmanager

logging.config.fileConfig(fname='log.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up the application...")
    # SQLModel.metadata.create_all(engine)
    yield
    logger.info("Shutting down the application...")

app = FastAPI(lifespan=lifespan)