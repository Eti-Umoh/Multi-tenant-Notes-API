from fastapi import APIRouter, status
from server.organizations.models import OrganizationCreate
from server.db import db
from server.main_utils import resource_conflict_response, created_response
from datetime import datetime, timezone
from server.authentication.utils import generate_random_password
import bcrypt

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
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
        "organization": {
            "id": str(org["_id"]),
            "name": org["name"],
            "description": org["description"],
            "created_at": org["created_at"],
        },
        "super_admin": {
            "email_address": admin_email,
            "password": admin_password,
        }
    }

    return created_response(message="successfully created org",
                            body=data_dict)
