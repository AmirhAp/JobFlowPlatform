from fastapi import FastAPI
from app.api.company_routes import router as company_router
from app.api.post_routes import router as posts_router
from app.api.person_routes import router as person_router
from app.db.session import Base, engine
from app.models import company, person, post
from app.core.logger import set_logger


app = FastAPI()


Base.metadata.create_all(bind=engine)
set_logger()

app.include_router(company_router)
app.include_router(posts_router)
app.include_router(person_router)