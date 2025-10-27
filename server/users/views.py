from fastapi import APIRouter, status
from server.users.models import UserCreate
from server.db import db
from server.main_utils import (resource_conflict_response, created_response,
                               resource_not_found_response, un_authenticated_response,
                               un_authorized_response)
from datetime import datetime, timezone
from server.authentication.utils import generate_random_password, authorize_jwt_subject
import bcrypt
from fastapi.params import Depends
from bson import ObjectId


router = APIRouter()


@router.post('/{org_id}/users')
async def create_user(org_id: str, payload: UserCreate,
                      token: str = Depends(authorize_jwt_subject)):
    email_address = token  # From authorize_jwt_subject, we get the subject which is the email

    current_user = await db.users.find_one({"email": email_address})
    if not current_user:
        msg = "User not found, Please Log In"
        return un_authenticated_response(msg)
    
    if current_user["organization_id"] != org_id:
        msg = "Only Admins can add a new admin"
        return un_authorized_response(msg)
    
    # ensure org exists
    org = await db.organizations.find_one({"_id": ObjectId(org_id)})
    if not org:
        return resource_not_found_response("Organization not found")

    existing = await db.users.find_one({"email": payload.email})
    if existing:
        raise HTTPException(409, "Email already exists")
    
    if current_user.user_type != UserTypes.ADMIN:
        msg = "Only Admins can add a new admin"
        return un_authenticated_response(msg)
    
    if not current_user.role:
        msg = "You have no role or permissions assigned to you"
        return un_authenticated_response(msg)
    
    role = await get_role_by_id(current_user.role, db)
    if "can create admin user" not in role.permissions:
        msg = "You do not have the permission to create admin user"
        return un_authenticated_response(msg)
    
    if payload.role:
        if "can assign role to admin user" not in role.permissions:
            msg = "You do not have the permission to assign role to admin user"
            return un_authenticated_response(msg)

    existing_user = await get_user_by_email(payload.email_address.lower(), db)
    if existing_user:
        msg = f"User with that email already exist"
        return resource_conflict_response(msg)
    
    existing_user = await get_user_by_phone(payload.phone_number, db)
    if existing_user:
        msg = f"User with that phone number already exist"
        return resource_conflict_response(msg)
    
    password = str(uuid.uuid4().hex)[:8]
    # Convert password to bytes and hash it
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt).decode('utf-8') 

    admin = await create_admin(
        payload.first_name, payload.last_name, payload.email_address.lower(),
        hashed_password, payload.phone_number, payload.gender, payload.role, db=db)
    if not admin:
        msg = "Create Admin failed"
        return internal_server_error_response(msg)
    
    link = settings.ADMIN_BASE_URL
    recipient = admin.email_address
    subject = "Account Created"
    content = await welcome_admin(admin, password, link)
    email_response = await send_email(recipient, subject, content)

    return created_response(message="success", body=await admin_serializer(admin, db))
