from datetime import datetime

from app.db.contact_repository import ContactRepository, contact_repository
from app.domain.contact import Contact
from app.dto.contact_dto import ContactCreate, ContactPatch, ContactUpdate, SortField, SortOrder

class ContactService:
    def __init__(self, repository: ContactRepository):
        self._repo = repository

    def create(self, data: ContactCreate) -> Contact:
        contact = Contact(**data.model_dump())
        return self._repo.add(contact)

    def get_by_id(self, contact_id: int) -> Contact | None:
        return self._repo.get_by_id(contact_id)
    
    def get_all(self,
                search: str | None = None,
                favorite: bool | None = None,
                sort: SortField = "name",
                order: SortOrder = "asc") -> list[Contact]:
        contacts = self._repo.get_all()
        if favorite is not None:
            contacts = [contact for contact in contacts if contact.is_favorite == favorite]
        if search is not None:
            search_lower = search.lower()
            contacts = [contact for contact in contacts if self._matches(contact, search_lower)]
        return sorted(contacts,
                      key=lambda contact: self._sort_key(contact, sort),
                      reverse=(order == "desc"))

    def _sort_key(self, contact: Contact, sort: SortField) -> tuple[str, str] | datetime:
        if sort == "created_at":
            return contact.created_at
        return (contact.first_name.lower(), contact.last_name.lower())

    def _matches(self, contact: Contact, term: str) -> bool:
        full_name = f"{contact.first_name} {contact.last_name}"
        if term in full_name.lower():
            return True
        if contact.email is not None and term in contact.email.lower():
            return True
        if contact.phone is not None and term in contact.phone.lower():
            return True
        return False

    def delete(self, contact_id: int) -> bool:
        return self._repo.delete(contact_id)
    
    def update(self, contact_id: int, data: ContactUpdate) -> Contact | None:
        updated_contact = Contact(**data.model_dump())
        return self._repo.update(contact_id, updated_contact)
    
    def patch(self, contact_id: int, data: ContactPatch) -> Contact | None:
        existing_contact = self._repo.get_by_id(contact_id)
        if existing_contact is None:
            return None

        # Update only the fields that are provided in the patch data
        updated_data = data.model_dump(exclude_unset=True)
        for key, value in updated_data.items():
            setattr(existing_contact, key, value)

        return self._repo.update(contact_id, existing_contact)
        

contact_service = ContactService(contact_repository)