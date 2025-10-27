from fastapi import APIRouter, status
from server.organizations.models import OrganizationCreate
from server.db import db
from server.main_utils import (resource_conflict_response, created_response,
                               resource_not_found_response, un_authenticated_response,
                               un_authorized_response, bad_request_response)
from datetime import datetime, timezone
from server.authentication.utils import generate_random_password, authorize_jwt_subject
import bcrypt
from server.users.models import UserCreate
from fastapi.params import Depends
from bson import ObjectId
from server.organizations.serializers import org_serializer
from server.users.serializers import user_serializer

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_organization(payload: OrganizationCreate):
    # check if organization already exists
    existing = await db.organizations.find_one({"name": payload.name})
    if existing:
        return resource_conflict_response("Organization already exists") 

    # create the organization document
    org_doc = payload.model_dump()
    org_doc["created_at"] = org_doc["updated_at"] = datetime.now(timezone.utc)
    result = await db.organizations.insert_one(org_doc)
    org_id = result.inserted_id

    # Create initial admin user
    admin_email = f"admin@{payload.name.lower().replace(' ', '')}.com"
    admin_password = generate_random_password(10)
    hashed = bcrypt.hashpw(admin_password.encode(), bcrypt.gensalt()).decode()
    
    admin_user = {
        "first_name": "Super",
        "last_name": "Admin",
        "email_address": admin_email,
        "password": hashed,
        "role": "admin",
        "organization_id": org_id,
        "created_at": datetime.now(timezone.utc),
    }

    await db.users.insert_one(admin_user)
    org = await db.organizations.find_one({"_id": org_id})

    data_dict = {
        "organization": await org_serializer(org),
        "super_admin": {
            "email_address": admin_email,
            "password": admin_password,
        }
    }

    return created_response(message="successfully created org",
                            body=data_dict)


@router.post('/{org_id}/users', status_code=status.HTTP_201_CREATED)
async def create_user(org_id: str, payload: UserCreate,
                      token: str = Depends(authorize_jwt_subject)):
    email_address = token  # From authorize_jwt_subject, we get the subject which is the email

    current_user = await db.users.find_one({"email": email_address})
    if not current_user:
        msg = "Please Log In"
        return un_authenticated_response(msg)
    
    # ensure org exists
    org = await db.organizations.find_one({"_id": ObjectId(org_id)})
    if not org:
        return resource_not_found_response("Organization not found")
    
    if current_user["organization_id"] != org_id:
        msg = f"You Are Not Part Of The Organization :{org_id}"
        return un_authorized_response(msg)
    
    if current_user["role"] != "admin":
        msg = "Only Admins can add new users"
        return un_authorized_response(msg)

    existing = await db.users.find_one({"email": payload.email_address})
    if existing:
        return resource_conflict_response("Email Already Exists")
    
    if payload.role not in ("reader", "writer", "admin"):
        return bad_request_response("Invalid 'role' specified")
    
    # Convert password to bytes and hash it
    password = generate_random_password(10)
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    # create the organization document
    user_doc = payload.model_dump()
    user_doc["organization_id"] = org_id
    user_doc["created_at"] = datetime.now(timezone.utc)
    user_doc["password"] = hashed
    result = await db.users.insert_one(user_doc)
    user_id = result.inserted_id
    user = await db.users.find_one({"_id": user_id})

    data_dict = {
        "user": await user_serializer(user),
        "password": password
    }
    return created_response(message="success", body=data_dict)
