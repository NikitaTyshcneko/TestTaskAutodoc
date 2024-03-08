**Inventory management system**

Simple inventory management system for a cyberpunk-themed game using FastAPI, SQLAlchemy, and PostgreSQL.

**Copy code**
```
git clone https://github.com/NikitaTyshcneko/TestTaskAutodoc.git
cd TestTaskAutodoc
```

**Install dependencies:**
```
pip install -r requirements.txt
```
**Apply migrations:**
```
alembic init alembic_name
alembic revision --autogenerate -m "your_migration_message"
alembic update head
```

**Run the Django development server:**
```
uvicorn main:app --reload 
```

Access the web UI at http://127.0.0.1:8000 in your browser.

**API Endpoints**

GET /docs/: Swagger documentation

POST /api/v1/refresh-token/: Refresh token

POST /api/v1/user/login/: User Login

**User**

GET /api/v1/user/get/: Get user by id

GET /api/v1/user/getall/: Get list of all users

POST /api/v1/user/register/: Register user

PUT  /api/v1/user/update/: Update user data

DELETE /api/v1/user/delete/: Delete user

**Item**

GET /api/v1/item/get/: Get item by id

GET /api/v1/item/getall/: Get list of all items

POST /api/v1/item/add/: Add item

PUT  /api/v1/item/update/: Update item

DELETE /api/v1/item/delete/: Delete item

GET /api/v1/user-item/all/: Get list of all user's items

POST /api/v1/user-item/add/: Add item to user's inventory

DELETE /api/v1/user-item/delete/: Delete item from user's inventory

**Dockerization**
The application is containerized using Docker for easy deployment and scalability. Use the provided Dockerfile to build the Docker image.
```
docker-compose up --build 
```