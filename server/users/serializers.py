from server.main_utils import to_ui_readable_datetime_format


async def user_serializer(user):
    items = {
        "id": str(user["_id"]),
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "email_address": user["email_address"],
        "role": user["role"],
        "organization_id": str(user["organization_id"]),
        "created_at": to_ui_readable_datetime_format(user["created_at"]),
    }
    return items


async def users_serializer(users):
    records = []
    for user in users:
        records.append(await user_serializer(user))
    return records
