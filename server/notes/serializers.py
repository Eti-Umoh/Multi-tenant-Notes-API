from server.main_utils import to_ui_readable_datetime_format


async def note_serializer(note):
    items = {
        "id": str(note["_id"]),
        "title": note["title"],
        "content": note["content"],
        "created_by": str(note["created_by"]),
        "organization_id": str(note["organization_id"]),
        "created_at": to_ui_readable_datetime_format(note["created_at"])
    }
    return items


async def notes_serializer(notes):
    records = []
    for note in notes:
        records.append(await note_serializer(note))
    return records
