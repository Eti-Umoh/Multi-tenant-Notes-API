from fastapi import APIRouter, status
from server.db import db
from server.main_utils import (give_pagination_details, success_response,
                               un_authenticated_response)
from server.authentication.utils import authorize_jwt_subject
from fastapi.params import Depends
from server.users.serializers import users_serializer
from fastapi_pagination import Params, paginate
from typing import Optional

router = APIRouter()


@router.get('', status_code=status.HTTP_200_OK)
async def get_users_by_org(token: str = Depends(authorize_jwt_subject),
                           page: Optional[int] = 1, page_by: Optional[int] = 20):
    email_address = token  # From authorize_jwt_subject, we get the subject which is the email

    current_user = await db.users.find_one({"email_address": email_address})
    if not current_user:
        msg = "User not found"
        return un_authenticated_response(msg)

    # Fetch users belonging to the organization
    users_cursor = db.users.find({"organization_id": current_user["organization_id"]})
    users = await users_cursor.to_list(length=page_by)

    paginated_users = paginate(users, params=Params(page=page, size=page_by))
    pagination_details = give_pagination_details(paginated_users)

    return success_response(
        message="Successfully retrieved users",
        body=await users_serializer(users),
        pagination=pagination_details
    )
