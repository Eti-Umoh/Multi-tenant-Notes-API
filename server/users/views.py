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



