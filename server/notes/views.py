from fastapi import APIRouter, status
from server.users.models import UserCreate
from server.db import db
from server.main_utils import (give_pagination_details, success_response,
                               un_authenticated_response)
from datetime import datetime, timezone
from server.authentication.utils import authorize_jwt_subject
from bson import ObjectId
from fastapi.params import Depends
from server.users.serializers import users_serializer
from fastapi_pagination import Params, paginate
from typing import Optional

router = APIRouter()


@router.post('', status_code=status.HTTP_201_CREATED)
async def create_note(payload: NoteCreate,
                      token: str = Depends(authorize_jwt_subject)):
    email_address = token  # From authorize_jwt_subject, we get the subject which is the email

    current_user = await db.users.find_one({"email_address": email_address})
    if not current_user:
        msg = "User not found"
        return un_authenticated_response(msg)
    
    # ensure org exists
    org = await db.organizations.find_one({"_id": ObjectId(org_id)})
    if not org:
        return resource_not_found_response("Organization not found")
    
    if str(current_user["organization_id"]) != org_id:
        msg = f"You Are Not Part Of The Organization :{org_id}"
        return un_authorized_response(msg)
    
    if current_user["role"] != "admin":
        msg = "Only Admins can add new users"
        return un_authorized_response(msg)

    existing = await db.users.find_one({"email_address": payload.email_address})
    if existing:
        return resource_conflict_response("Email Already Exists")
    
    # Convert password to bytes and hash it
    password = generate_random_password(10)
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    # create the organization document
    user_doc = payload.model_dump()
    user_doc["organization_id"] = ObjectId(org_id)
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
