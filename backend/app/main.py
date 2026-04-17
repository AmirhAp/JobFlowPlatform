from fastapi import FastAPI
from app.api.company import router as company_router
from app.api.posts import router as posts_router
from app.api.persons import router as person_router


app = FastAPI()

app.include_router(company_router)
app.include_router(posts_router)
app.include_router(person_router)