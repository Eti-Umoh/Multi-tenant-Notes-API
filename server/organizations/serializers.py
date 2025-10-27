from server.main_utils import to_ui_readable_datetime_format


async def org_serializer(org):
    items = {
        "id": str(org["_id"]),
        "name": org["name"],
        "description": org["description"],
        "created_at": to_ui_readable_datetime_format(org["created_at"]),
        "updated_at": to_ui_readable_datetime_format(org["updated_at"]),
    }
    return items


async def orgs_serializer(orgs):
    records = []
    for org in orgs:
        records.append(await org_serializer(org))
    return records