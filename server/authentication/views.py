from fastapi import APIRouter, Request, status
from server.authentication.schemas import LoginUser
from server.db import db
import bcrypt
from server.main_utils import (un_authorized_response, success_response,
                               internal_server_error_response)
from server.authentication.utils import create_access_token

router = APIRouter()


@router.post('/login', status_code=status.HTTP_200_OK)
async def login_user(request: Request, payload: LoginUser):
    user = await db.users.find_one({"email_address": payload.email_address})
    if user:
        # Convert password to bytes
        password_bytes = payload.password.encode()
        hashed_password = user["password"].encode()

    if not user or not bcrypt.checkpw(password_bytes, hashed_password):
        msg = "Invalid Email or Password"
        return un_authorized_response(msg)

    access_token = create_access_token(user.email_address)
    if not access_token:
        msg = "Error generating access token"
        return internal_server_error_response(msg)

    return success_response(message="successful",
                            body={"user": user,
                                  "access-token": access_token,
                                  "token_type": "bearer"})
