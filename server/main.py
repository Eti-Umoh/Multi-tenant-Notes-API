from fastapi import FastAPI, Request, status, HTTPException
from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from server.users.views import router as UserRouter
from server.authentication.views import router as AuthRouter
from server.organizations.views import router as OrgRouter
from server.notes.views import router as NoteRouter
from server.config import settings
from server.main_utils import error_response, resource_not_found_response
from server.db import db
from bson import ObjectId
from server.authentication.utils import authorize_jwt_subject


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


# Initialize FastAPI
app = FastAPI(
    title="Multi-tenant Notes API",
    description="A multi-tenant Notes API where multiple organizations can manage their users\
        and notes independently, with strict role-based access control",
    openapi_tags=tags_metadata
)


#MIDDLEWARE THAT AUTOMATICALLY EXTRACT TENANT/USER FROM HEADERS
@app.middleware("http")
async def authentication_middleware(request: Request, call_next):
    def get_data(msg):
        return {"detail": msg}
    
    routes_without_auth = ["/api/v1/organizations", "/api/v1/auth/login"]

    if not request.url.path == "/api/v1/organizations":
        org_id = request.headers.get('org_id')
        if not org_id:
            msg = "org_id is missing in the request headers"
            return error_response(status.HTTP_400_BAD_REQUEST,
                                    get_data(msg))
        
        # ensure org exists
        org = await db.organizations.find_one({"_id": ObjectId(org_id)})
        if not org:
            msg = "Invalid org_id specified in the request headers"
            return error_response(status.HTTP_400_BAD_REQUEST, get_data(msg))
        
        # Attach org to request.state
        request.state.org = org #EXTRACT TENANT
        
    if request.url.path not in routes_without_auth:
        try:
            # Extract token manually from header
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                msg = "Missing or invalid Authorization header"
                return error_response(status.HTTP_401_UNAUTHORIZED, get_data(msg))

            token = auth_header.split(" ")[1]
            email_address = authorize_jwt_subject(token)

        except HTTPException as e:
            return error_response(e.status_code, get_data(e.detail))
        except Exception as e:
            msg = "Invalid or expired token"
            return error_response(status.HTTP_401_UNAUTHORIZED, get_data(msg))

        # Get user from DB
        current_user = await db.users.find_one({
            "email_address": email_address,
            "organization_id": ObjectId(org_id)
            })
        if not current_user:
            msg = "User not found"
            return error_response(status.HTTP_401_UNAUTHORIZED, get_data(msg))

        # Attach user to request.state
        request.state.user = current_user #EXTRACT USER
    
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
