# 📝 Multi-Tenant Notes API

A FastAPI-based **multi-tenant Notes API** where multiple organizations can manage their users and notes independently — with strict **role-based access control (RBAC)**.


## 🚀 Features
- Multi-tenancy with organization isolation
- Role-based permissions (`reader`, `writer`, `admin`)
- JWT authentication
- Automatic admin user creation per organization
- Email notification for new user credentials (via Mailjet)
- Docker support for local deployment
- Async MongoDB (Motor)
- Unit tests using `pytest` and `httpx`


## 🧠 Core Requirements Implemented
**Organizations** - Create new organizations (tenants). 
**Users** - Create users under specific organizations with roles (`reader`, `writer`, `admin`). 
**Notes** - CRUD operations based on roles. Notes are scoped per organization. 
**Access Control** - Role-based logic ensures isolation between organizations. 
**Testing** - Includes automated test with `pytest`. 
**Dockerized** - App runs fully via Docker for easy setup. 


## ⚙️ Tech Stack
- **Python** (programming language)
- **FastAPI** (backend framework)
- **MongoDB Atlas** (database)
- **Motor** (async MongoDB driver)
- **Mailjet API** (email service)
- **Docker & Docker Compose** (running)
- **Pytest + HTTPX** (testing)


## Instructions to run your app locally (or via Docker)
1. Clone the repository, then run the command:
    **cd Multi-tenant-Notes-API**

2. Create a virtual environment (optional) with this command:
    python -m venv venv
  Activate if necessary:
    source venv/bin/activate   # (Mac/Linux)
    venv\Scripts\activate      # (Windows)

3. Install dependencies with this command:
    **pip install -r requirements.txt**

4. Configure environment variables, Create a .env file.
    Copy from .env.example and Update the values with your values

5. Run with Docker the command:
    **docker compose up --build**
  OR Run locally with the command:
    **uvicorn server.main:app**

6. Run tests with this command:
    **python -m pytest -v**  


You can test the API via **Postman**
### 👉 Using Postman
Import the Postman collection file provided in this Github Repository:
[`Multi-tenant note API.postman_collection.json`]

#### How to use:
1. Open Postman.
2. Click **Import** → **File**.
3. Select the downloaded `Multi-tenant note API.postman_collection.json`.
4. Run the requests directly.


**NOTE:** - While working with Postman, all requests except "create org" require an "org_id" in the headers.
All requests except "create org" and "login" require a bearer token in the headers. 

**NOTE** - While running tests with **python -m pytest -v** ,
In tests/test_notes.py, the 3rd endpoint in the test function will always fail if "email_address" is reused OR
if the credentials from the 2nd endpoint are not for an admin user
