from fastapi import FastAPI
from app.api.company import router as company_router
from app.api.posts import router as posts_router
from app.api.persons import router as person_router
from app.db.session import Base, engine
from app.models import company


app = FastAPI()


Base.metadata.create_all(bind=engine)


app.include_router(company_router)
app.include_router(posts_router)
app.include_router(person_router)