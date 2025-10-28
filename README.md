# 📝 Multi-Tenant Notes API

A FastAPI-based **multi-tenant Notes API** where multiple organizations can manage their users and notes independently — with strict **role-based access control (RBAC)**.


## 🚀 Features
- Multi-tenancy with organization isolation
- Role-based permissions (`reader`, `writer`, `admin`)
- JWT authentication
- Automatic admin user creation per organization
- Docker support for local deployment
- Async MongoDB (Motor)
- Unit tests using `pytest` and `httpx`


**Additions Made**
- Email notification for new user credentials (via Mailjet)
- Endpoint to retrieve all users of an organization
- Access Control for "Create User" endpoint (Only Admins can create a new user)


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


## Instructions to run the app locally (or via Docker)
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

5. Run with Docker with the command:
    **docker compose up --build**
  OR Run locally with the command:
    **uvicorn server.main:app**

6. Run tests with this command:
    **python -m pytest -v**  


You can test the API via **Postman**
## 👉 Using Postman
Import the Postman collection file provided in this Github Repository:
[`Multi-tenant note API.postman_collection.json`]

## How to use:
1. Open Postman.
2. Click **Import** → **File**.
3. Select the downloaded `Multi-tenant note API.postman_collection.json`.
4. Run the requests directly.


**NOTE:** - While working with Postman, all requests except "create organization" require an "org_id" in the headers.
All requests except "create organization" and "login" require a bearer token in the headers. 

**NOTE** - While running tests with **python -m pytest -v** , In tests/test_notes.py,
the 3rd endpoint (create user) in the "test_create_and_get_notes" function will cause the test to fail if the same "email_address"
is used in the "user_payload" more than once, this is because an organization can not have users with the same email address.
Also, for the 2nd endpoint (login) in the "test_create_and_get_notes" function, if the credentials in the "login_payload" are not
for an admin user the test will fail, this is because only an admin user can create a new user in the 3rd endpoint.
