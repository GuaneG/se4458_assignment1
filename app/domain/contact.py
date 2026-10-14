from dataclasses import dataclass, field
from datetime import datetime, timezone

@dataclass(kw_only=True)
class Contact:
    id: int | None = None          # repository'ye eklenince atanır
    first_name: str
    last_name: str
    email: str | None = None
    phone: str | None = None
    is_favorite: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))