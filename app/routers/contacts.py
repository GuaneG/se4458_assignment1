from fastapi import APIRouter, HTTPException, status
from app.dto.contact_dto import (ContactCreate, ContactPatch, ContactResponse, ContactUpdate,
                                 SortField, SortOrder)
from app.services.contact_service import contact_service

router = APIRouter(prefix="/api/v1/contacts", tags=["Contacts"])


@router.post("", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
def create_contact(data: ContactCreate):
    return contact_service.create(data)

@router.get("", response_model=list[ContactResponse])
def list_contacts(search: str | None = None,
                  favorite: bool | None = None,
                  sort: SortField = "name",
                  order: SortOrder = "asc"):
    return contact_service.get_all(search=search, favorite=favorite, sort=sort, order=order)

@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(contact_id: int):
    if not contact_service.delete(contact_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Contact {contact_id} not found")

@router.get("/{contact_id}", response_model=ContactResponse)
def get_contact(contact_id: int):
    contact = contact_service.get_by_id(contact_id)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Contact {contact_id} not found")
    return contact

@router.put("/{contact_id}", response_model=ContactResponse)
def update_contact(contact_id: int, data: ContactUpdate):
    updated_contact = contact_service.update(contact_id, data)
    if updated_contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Contact {contact_id} not found")
    return updated_contact

@router.patch("/{contact_id}", response_model=ContactResponse)
def patch_contact(contact_id: int, data: ContactPatch):
    updated_contact = contact_service.patch(contact_id, data)
    if updated_contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Contact {contact_id} not found")
    return updated_contact