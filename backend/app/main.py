from fastapi import FastAPI, Request
import uuid
import logging

from app.api.company_routes import router as company_router
from app.api.post_routes import router as posts_router
from app.api.person_routes import router as person_router
from app.db.session import Base, engine
from app.models import company, person, post
from app.core.logger import set_logger


app = FastAPI()

Base.metadata.create_all(bind=engine)
set_logger()


logger = logging.getLogger(__name__)

@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4)

    request.state.request_id = request_id
    logger.info(f"{request_id} is started!!")

    respone = await call_next(request)

    logger.info(f"{request_id} is done")

    return respone


app.include_router(company_router)
app.include_router(posts_router)
app.include_router(person_router)