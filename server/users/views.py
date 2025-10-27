from fastapi import APIRouter, status
from server.users.models import UserCreate
from server.db import db
from server.main_utils import (give_pagination_details,
                               resource_not_found_response,
                               success_response)
from datetime import datetime, timezone
from server.authentication.utils import authorize_jwt_subject
from bson import ObjectId
from fastapi.params import Depends
from server.users.serializers import users_serializer
from fastapi_pagination import Params, paginate
from typing import Optional


router = APIRouter()


@router.get("/{org_id}", status_code=status.HTTP_200_OK)
async def get_users_by_org(org_id: str, token: str = Depends(authorize_jwt_subject),
                           page: Optional[int] = 1, page_by: Optional[int] = 20,):
    # Ensure org exists
    org = await db.organizations.find_one({"_id": ObjectId(org_id)})
    if not org:
        return resource_not_found_response("Organization not found")

    # Fetch users belonging to the organization
    users_cursor = db.users.find({"organization_id": ObjectId(org_id)})
    users = await users_cursor.to_list(length=page_by)

    paginated_users = paginate(users, params=Params(page=page, size=page_by))
    pagination_details = give_pagination_details(paginated_users)

    return success_response(
        message="Successfully retrieved users",
        body=await users_serializer(users)
    )
