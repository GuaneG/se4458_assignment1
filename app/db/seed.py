from app.db.contact_repository import ContactRepository
from app.domain.contact import Contact

SEED_CONTACTS = [
    {"first_name": "Alan", "last_name": "Turing", "email": "alan.turing@auning.com",
     "phone": "+1 555 123 4567", "is_favorite": True},
    {"first_name": "Marie", "last_name": "Curie", "email": "marie.curie@mail.com"},
    {"first_name": "Katherine", "last_name": "Johnson", "email": "katherine.johnson@abcc.com",
     "is_favorite": True},
    {"first_name": "Charles", "last_name": "Darwin", "email": "charles.darwin@adl.gov"},
    {"first_name": "Ada", "last_name": "Lovelace", "email": "ada.lovelace@mail.com",
     "phone": "+44 20 7946 0958", "is_favorite": True},
    {"first_name": "Grace", "last_name": "Hopper", "phone": "+1 555 987 6543"},
]


def seed(repository: ContactRepository) -> None:
    for data in SEED_CONTACTS:
        repository.add(Contact(**data))
