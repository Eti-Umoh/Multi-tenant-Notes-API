from fastapi import APIRouter, Request

router = APIRouter()


# server/users/views.py
from fastapi import APIRouter, HTTPException, status
from server.users.utils import create_user, get_user_by_email, get_user_by_phone
from server.organizations.models import OrganizationCreate

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def provision_organization(payload: OrganizationCreate):
    # Check duplicates
    existing_user = await get_user_by_email(payload.email_address.lower())
    if existing_user:
        raise HTTPException(status_code=409, detail="User with that email already exists")

    existing_phone = await get_user_by_phone(payload.phone_number)
    if existing_phone:
        raise HTTPException(status_code=409, detail="User with that phone number already exists")

    # Create user
    new_user = await create_user(payload)
    if not new_user:
        raise HTTPException(status_code=500, detail="Create user failed")

    return {
        "message": "User created successfully",
        "data": new_user
    }
