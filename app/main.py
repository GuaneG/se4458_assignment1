from fastapi import FastAPI
from app.db.contact_repository import contact_repository
from app.db.seed import seed
from app.routers import contacts

app = FastAPI(title="Address Book API", version="1.0.0")
app.include_router(contacts.router)

seed(contact_repository)
