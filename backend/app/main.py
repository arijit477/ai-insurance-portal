from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings


from app.database.db import Base, engine
from app.api.routes import auth, users, admin
from app.api.routes import insurance_plan
from app.api.routes import policy
from app.api.routes import claim
from app.api.routes import claim_image
from app.api.routes import claim_document
from app.api.routes import upload
from app.api.routes import ai
from app.api.routes import dashboard
from app.api.routes import chat

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Insurance Portal",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(admin.router)
app.include_router(insurance_plan.router)
app.include_router(policy.router)
app.include_router(claim.router)
app.include_router(claim_image.router)
app.include_router(claim_document.router)
app.include_router(upload.router)
app.include_router(ai.router)
app.include_router(
    dashboard.router,
    prefix=settings.API_V1_STR,
)

app.include_router(
    chat.router,
    prefix=settings.API_V1_STR,
)


@app.get("/")
def root():
    return {"message": "AI Insurance Portal API Running"}
