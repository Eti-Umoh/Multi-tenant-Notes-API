from fastapi import APIRouter, status, Request
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
async def get_users_by_org(request: Request, page: Optional[int] = 1,
                           page_by: Optional[int] = 20):
    org = request.state.org 

    # Fetch users belonging to the organization
    users_cursor = db.users.find({"organization_id": org["_id"]})
    users = await users_cursor.to_list(length=page_by)

    paginated_users = paginate(users, params=Params(page=page, size=page_by))
    pagination_details = give_pagination_details(paginated_users)

    return success_response(
        message="Successfully retrieved users",
        body=await users_serializer(users),
        pagination=pagination_details
    )
