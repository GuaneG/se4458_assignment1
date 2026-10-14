from app.domain.contact import Contact

class ContactRepository:
    def __init__(self):
        self._contacts: dict[int, Contact] = {}
        self._next_id = 1

    def add(self, contact: Contact) -> Contact:
        contact.id = self._next_id
        self._contacts[contact.id] = contact
        self._next_id += 1
        return contact

    def get_by_id(self, contact_id: int) -> Contact | None:
        return self._contacts.get(contact_id)   # yoksa KeyError değil None döner

    def get_all(self) -> list[Contact]:
        # TODO: sen yaz
        return list(self._contacts.values())

    def update(self, contact_id: int, contact: Contact) -> Contact | None:
        # TODO: sen yaz. Yoksa None dön; varsa id'yi ve created_at'i koru, kaydı değiştir
        existing_contact = self._contacts.get(contact_id)
        if existing_contact is None:
            return None

        # id ve created_at değerlerini koru
        contact.id = existing_contact.id
        contact.created_at = existing_contact.created_at

        self._contacts[contact_id] = contact
        return contact

    def delete(self, contact_id: int) -> bool:
        # TODO: sen yaz. Silindiyse True, yoksa False
        return self._contacts.pop(contact_id, None) is not None


# Uygulama boyunca tek instance: "in-memory database" tam olarak bu
contact_repository = ContactRepository()