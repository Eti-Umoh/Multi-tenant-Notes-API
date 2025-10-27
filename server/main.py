from fastapi import FastAPI, Request, status
from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from server.users.views import router as UserRouter
from server.authentication.views import router as AuthRouter
from server.organizations.views import router as OrgRouter
from server.notes.views import router as NoteRouter
from server.config import settings
from server.main_utils import error_response
from server.db import db


tags_metadata = [
    {
        "name": "users"
    },
    {
        "name": "notes"
    },
    {
        "name": "organizations"
    },
]


# Initialize FastAPI with the lifespan handler
app = FastAPI(
    title="Multi-tenant Notes API",
    description="A multi-tenant Notes API where multiple organizations can manage their users\
        and notes independently, with strict role-based access control",
    openapi_tags=tags_metadata
)


@app.middleware("http")
async def authentication_middleware(request: Request, call_next):
    def get_data(msg):
        return {"detail": msg}
    
    response = await call_next(request)
    return response


origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


api_router = APIRouter(prefix="/api/v1")

api_router.include_router(UserRouter, tags=['users'],
                          prefix="/users")
api_router.include_router(OrgRouter, tags=['organizations'],
                          prefix="/organizations")
api_router.include_router(AuthRouter, tags=['auth'],
                          prefix="/auth")
api_router.include_router(NoteRouter, tags=['notes'],
                          prefix="/notes")

app.include_router(api_router)


@app.get("/", tags=["Root"])
async def read_root() -> dict:
    return {"message": "Multi-tenant Notes API!"}


@app.get("/test-db")
async def test_db():
    collections = await db.list_collection_names()
    return {"collections": collections}
