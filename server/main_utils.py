from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from http import HTTPStatus
import pytz
from datetime import datetime



def bad_request_response(msg):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)


def un_authorized_response(msg):
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=msg)


def un_authenticated_response(msg):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=msg)


def resource_conflict_response(msg):
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=msg)


def resource_not_found_response(msg):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)


def internal_server_error_response(msg):
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg)


def error_response(http_status_code, data):
    return JSONResponse(data, status_code=http_status_code)


# success responses
def created_response(message="", body=None):
    return success_response(message=message, body=body, status=HTTPStatus.CREATED)


def success_response(message="", body=None, pagination=None, kwargs=None, need_list=None, status=None):
    if not body:
        if need_list:
            body = []
        else:
            body = {}
    response_data = {}
    response_data['data'] = body
    response_data['message'] = message

    if pagination:
        response_data['pagination'] = pagination
        if not response_data['data']:
            response_data['data'] = []

    response = JSONResponse(response_data)
    if status:
        response = JSONResponse(response_data, status)

    return response


def to_ui_readable_datetime_format(value):
    try:
        if value is None:
            return ""

        timezone = pytz.timezone('Africa/Lagos')
        localized_value = value.astimezone(timezone)
        return localized_value.strftime("%b %d, %Y %I:%M%p")
    except Exception as ex:
        print(ex)
        return str(value)
    

def give_pagination_details(paginator):
    return {
        "total_pages": paginator.pages,
        "limit": paginator.size,
        "count": paginator.total,
        "current_page": paginator.page,
    }
