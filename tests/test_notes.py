import pytest
from httpx import AsyncClient
from server.main import app  # or wherever your FastAPI app is created


@pytest.mark.asyncio
async def test_create_and_get_notes():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # 1️⃣ Create an organization
        org_payload = {"name": "TestOrg"}
        org_response = await ac.post("/api/v1/organizations", json=org_payload)
        assert org_response.status_code == 201
        org_data = org_response.json()["body"]["organization"]
        org_id = org_data["_id"]

        # 2️⃣ Create a user (admin)
        user_payload = {
            "first_name": "John",
            "last_name": "Doe",
            "email_address": "john@example.com",
            "password": "password123",
            "role": "admin"
        }
        user_response = await ac.post(f"/api/v1/organizations/{org_id}/users/", json=user_payload)
        assert user_response.status_code in (200, 201)

        # 3️⃣ Login and get token
        login_payload = {
            "email_address": "john@example.com",
            "password": "password123"
        }
        login_response = await ac.post("/api/v1/auth/login", data=login_payload)
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]

        headers = {"Authorization": f"Bearer {token}", "org_id": org_id}

        # 4️⃣ Create a note
        note_payload = {"title": "My First Note", "content": "This is a test note"}
        note_response = await ac.post("/api/v1/notes/", json=note_payload, headers=headers)
        assert note_response.status_code == 201

        # 5️⃣ Retrieve all notes
        notes_response = await ac.get("/api/v1/notes/", headers=headers)
        assert notes_response.status_code == 200
        notes = notes_response.json()["body"]
        assert len(notes) > 0
