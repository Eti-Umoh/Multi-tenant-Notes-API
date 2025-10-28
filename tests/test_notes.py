import pytest
from httpx import AsyncClient, ASGITransport
from server.main import app


@pytest.mark.asyncio
async def test_create_and_get_notes():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # 1️⃣ Create an organization
        org_payload = {"name": "TestOrg", "description": "test description of org",
                       "admin_email": "mister01@mailinator.com"}
        org_response = await ac.post("/api/v1/organizations", json=org_payload)
        org_data = org_response.json()["data"]
        assert org_response.status_code == 201

        # 2️⃣ Login and get token
        headers = {"org_id": "68ff992a0639bb282372c702"}
        login_payload = {
            "email_address": "admin@godolkin-four.com",
            "password": "uyugTDCQU6"
        }
        login_response = await ac.post("/api/v1/auth/login",
                                       json=login_payload, headers=headers)
        assert login_response.status_code == 200
        token = login_response.json()["data"]["access_token"]
        org_id = login_response.json()["data"]["user"]["organization_id"]

        # 3️⃣ Create a user (admin)
        headers = {"Authorization": f"Bearer {token}", "org_id": org_id}
        user_payload = {
            "first_name": "John",
            "last_name": "Doe",
            "email_address": "johndoe@mailinator.com",
            "role": "admin"
        }
        user_response = await ac.post(f"/api/v1/organizations/{org_id}/users",
                                      json=user_payload, headers=headers)
        assert user_response.status_code == 201

        # 4️⃣ Create a note
        note_payload = {"title": "Test Note", "content": "This is a test note"}
        note_response = await ac.post("/api/v1/notes", json=note_payload, headers=headers)
        assert note_response.status_code == 201

        # 5️⃣ Retrieve all notes
        notes_response = await ac.get("/api/v1/notes", headers=headers)
        assert notes_response.status_code == 200
        notes = notes_response.json()["data"]
        assert len(notes) > 0
