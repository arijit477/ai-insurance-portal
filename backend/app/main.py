from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
import os
from fastapi.staticfiles import StaticFiles


from app.database.db import Base, engine
from app.api.routes import auth, users, admin
from app.api.routes import insurance_plan
from app.api.routes import policy
from app.api.routes import claim
from app.api.routes import claim_image
from app.api.routes import claim_document
from app.api.routes import upload
from app.api.routes import ai
from app.api.routes import notification
from app.api.routes import dashboard
from app.api.routes import chat

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Insurance Portal",
    version="1.0.0",
)


@app.on_event("startup")
def on_startup():
    from app.database.db import SessionLocal
    from app.database.seed import seed_db
    db = SessionLocal()
    try:
        seed_db(db)
    finally:
        db.close()

import logging
from fastapi.responses import JSONResponse
from fastapi import Request

logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Global uncaught exception: %s", exc)
    response = JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error", "error": str(exc)},
    )
    origin = request.headers.get("origin")
    if origin:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Headers"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "*"
    return response


uploads_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

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
app.include_router(notification.router)
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
