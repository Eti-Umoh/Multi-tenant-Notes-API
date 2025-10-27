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
    token_condition = ((request.url.path.startswith("/api/v1/organizations"))
                       or (request.url.path.startswith("/api/v1/auth/login"))
                       )
    if token_condition:
        secret = request.headers.get('Secret')
        if not secret:
            msg = "Secret is missing in the request headers"
            return error_response(status.HTTP_400_BAD_REQUEST,
                                    get_data(msg))
        elif secret != settings.SECRET:
            msg = "Invalid Secret specified in the request headers"
            return error_response(status.HTTP_400_BAD_REQUEST,
                                    get_data(msg))

    org_id = request.headers.get('org_id')
    if not org_id:
        msg = "org_id is missing in the request headers"
        return error_response(status.HTTP_400_BAD_REQUEST,
                                get_data(msg))
    
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
