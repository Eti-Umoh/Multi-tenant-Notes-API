from fastapi import APIRouter, status, Request
from server.notes.models import NoteCreate
from server.db import db
from server.main_utils import (give_pagination_details, success_response,
                               un_authenticated_response, un_authorized_response,
                               created_response, bad_request_response,
                               resource_not_found_response)
from datetime import datetime, timezone
from server.authentication.utils import authorize_jwt_subject
from bson import ObjectId
from fastapi.params import Depends
from server.notes.serializers import note_serializer, notes_serializer
from fastapi_pagination import Params, paginate
from typing import Optional

router = APIRouter()


@router.post('', status_code=status.HTTP_201_CREATED)
async def create_note(request: Request, payload: NoteCreate):
    current_user = request.state.user
    if current_user["role"] not in ("admin", "writer"):
        msg = "Access Denied"
        return un_authorized_response(msg)

    # create the organization document
    note_doc = payload.model_dump()
    note_doc["organization_id"] = current_user["organization_id"]
    note_doc["created_at"] = datetime.now(timezone.utc)
    note_doc["created_by"] = current_user["_id"]
    result = await db.notes.insert_one(note_doc)
    note_id = result.inserted_id
    note = await db.notes.find_one({"_id": note_id})

    return created_response(message="success", body=await note_serializer(note))


@router.get('', status_code=status.HTTP_200_OK)
async def get_notes(token: str = Depends(authorize_jwt_subject),
                    page: Optional[int] = 1, page_by: Optional[int] = 20):
    email_address = token  # From authorize_jwt_subject, we get the subject which is the email

    current_user = await db.users.find_one({"email_address": email_address})
    if not current_user:
        msg = "User not found"
        return un_authenticated_response(msg)

    # Fetch notes belonging to the organization
    notes_cursor = db.notes.find({"organization_id": current_user["organization_id"]})
    notes = await notes_cursor.to_list(length=page_by)

    paginated_notes = paginate(notes, params=Params(page=page, size=page_by))
    pagination_details = give_pagination_details(paginated_notes)

    return success_response(message="success", body=await notes_serializer(notes),
                            pagination=pagination_details)


@router.get('/{note_id}', status_code=status.HTTP_200_OK)
async def get_note(note_id:str, token: str = Depends(authorize_jwt_subject)):
    email_address = token  # From authorize_jwt_subject, we get the subject which is the email

    current_user = await db.users.find_one({"email_address": email_address})
    if not current_user:
        msg = "User not found"
        return un_authenticated_response(msg)
    
    # Ensure note_id is a valid ObjectId
    if not ObjectId.is_valid(note_id):
        return bad_request_response("Invalid note ID")

    # Find note by both note_id and organization_id
    note = await db.notes.find_one({
        "_id": ObjectId(note_id),
        "organization_id": current_user["organization_id"]
    })
    if not note:
        return resource_not_found_response("Note not found")

    return success_response(message="success", body=await note_serializer(note))


@router.delete('/{note_id}', status_code=status.HTTP_200_OK)
async def delete_note(note_id:str, token: str = Depends(authorize_jwt_subject)):
    email_address = token  # From authorize_jwt_subject, we get the subject which is the email

    current_user = await db.users.find_one({"email_address": email_address})
    if not current_user:
        msg = "User not found"
        return un_authenticated_response(msg)
    
    if current_user["role"] != "admin":
        msg = "Access Denied"
        return un_authorized_response(msg)
    
    # Ensure note_id is a valid ObjectId
    if not ObjectId.is_valid(note_id):
        return bad_request_response("Invalid note ID")

    # Find note by both note_id and organization_id
    note = await db.notes.find_one({
        "_id": ObjectId(note_id),
        "organization_id": current_user["organization_id"]
    })
    if not note:
        return resource_not_found_response("Note not found")
    
    # Perform deletion
    await db.notes.delete_one({
        "_id": ObjectId(note_id),
        "organization_id": current_user["organization_id"]
    })

    return success_response(message="Note deleted successfully", body={})
