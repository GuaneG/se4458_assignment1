# Address Book REST API

SE4458 Assignment 2, Group 1. An in-memory REST API for an address book: create, edit, update, delete, search, sort and favorite contacts. Built with Python and FastAPI. There is no frontend; the API is documented and testable through Swagger UI.

| | Link |
|---|---|
| Source code | https://github.com/GuaneG/se4458_assignment1 |
| Live API (Swagger UI) | https://se4458-assignment1.onrender.com/docs |

> **If the live link does not open:**
> - The app runs on Render's free tier. After a period of inactivity it goes to sleep, so the first request can take up to a minute while it starts again.
> - Some networks in Turkey (including some ISPs and campus networks) block `*.onrender.com` addresses; the connection is reset before the page loads. If that happens, please try another network, such as mobile data, or a VPN.

## Endpoints

Base path: `/api/v1/contacts`

| Method | Path | Description | Success | Errors |
|---|---|---|---|---|
| `POST` | `/api/v1/contacts` | Create a contact | `201` + contact | `422` invalid body |
| `GET` | `/api/v1/contacts` | List contacts (search, filter, sort) | `200` + list | `422` invalid query |
| `GET` | `/api/v1/contacts/{id}` | Get one contact | `200` + contact | `404` |
| `PUT` | `/api/v1/contacts/{id}` | Edit: replace all fields | `200` + contact | `404`, `422` |
| `PATCH` | `/api/v1/contacts/{id}` | Update: change only the fields sent | `200` + contact | `404`, `422` |
| `DELETE` | `/api/v1/contacts/{id}` | Delete a contact | `204`, no body | `404` |

### Query parameters for `GET /api/v1/contacts`

| Parameter | Values | Default | Effect |
|---|---|---|---|
| `search` | any text | none | Case-insensitive substring match on full name, email or phone |
| `favorite` | `true` / `false` | none | Only favorites / only non-favorites |
| `sort` | `name` / `created_at` | `name` | `name` sorts by first name, then last name, case-insensitive |
| `order` | `asc` / `desc` | `asc` | Sort direction |

Example: `GET /api/v1/contacts?search=mail.com&favorite=true&sort=name&order=desc`

### Favorite

Favoriting is a partial update of one field:

```http
PATCH /api/v1/contacts/1
Content-Type: application/json

{ "is_favorite": true }
```

### Contact fields

| Field | Type | Rules |
|---|---|---|
| `first_name` | string | Required, 1–50 characters |
| `last_name` | string | Required, 1–50 characters |
| `email` | string or null | Optional, must be a valid email address |
| `phone` | string or null | Optional, free text |
| `is_favorite` | boolean | Optional, defaults to `false` |
| `id` | integer | Assigned by the server, response only |

## Design

### Layered architecture

The project follows the same layered structure as the course's to-do template ([southriver/apiNode](https://github.com/southriver/apiNode)). Each layer only talks to the layer below it.

```
app/
├── main.py                       app setup, router registration, seed data
├── routers/contacts.py           HTTP layer: routes, status codes, 404 handling
├── services/contact_service.py   business logic: search, filtering, sorting, PATCH merge
├── db/contact_repository.py      in-memory storage (a dict keyed by id)
├── db/seed.py                    sample contacts loaded at startup
├── domain/contact.py             internal Contact model (dataclass)
└── dto/contact_dto.py            request/response schemas and validation (Pydantic)
```

| Template file (Express) | This project (FastAPI) |
|---|---|
| `index.js` | `routers/contacts.py` |
| `services/todoService.js` | `services/contact_service.py` |
| `db/todoDBContext.js` | `db/contact_repository.py` |
| `domain/Todo.js` | `domain/contact.py` |
| `dto/*.js`, `DtoValidationError.js` | `dto/contact_dto.py` (Pydantic) |
| `docs/openapi.json` (hand-written) | Generated automatically by FastAPI at `/docs` |

Two parts that the template writes by hand come from the framework here: request validation (Pydantic) and the OpenAPI/Swagger document (FastAPI).

### Design decisions

- **One list endpoint with query parameters instead of a separate `/search` endpoint.** The template uses `GET /todos/search?keyword=...`. The address book screen combines search, a favorite filter and sorting at the same time, so all of them are optional query parameters on `GET /api/v1/contacts` and can be combined freely.
- **PUT and PATCH are separate.** `PUT` replaces the whole contact: fields that are not sent go back to their defaults. `PATCH` changes only the fields that are present in the request body. PATCH uses Pydantic's `model_dump(exclude_unset=True)` to tell "field not sent" apart from "field sent as `null`": sending `{"phone": null}` clears the phone, while leaving `phone` out keeps it.
- **`DELETE` returns `204 No Content`.** The template returns `200` with the deleted item. Both are common; `204` was chosen because the client already knows what it deleted.
- **Filtering and sorting live in the service layer.** The repository is a plain dict and only stores data. Which fields are searched and how results are ordered are business rules, so they belong in the service. With a real database these would move into the repository as a query.
- **Separate domain model and DTOs.** `Contact` (dataclass) is the internal model and also holds `created_at`. The DTOs define what clients may send and what they get back, so internal fields are not exposed by accident.
- **Validation errors return `422`.** This is FastAPI's default for invalid request bodies or query values (for example `sort=xyz`). The template returns `400`.
- **Layered monolith, not separate services.** There is a single resource (contacts) and the assignment asks for one public URL, so splitting the app into services would add network calls and deployment overhead without solving a real problem.

## Assumptions

- **"Edit" and "update"** in the assignment are interpreted as `PUT` (full edit, like the form's Save button) and `PATCH` (partial update, like toggling the favorite star).
- **Tags** from the UI mockup are out of scope. The assignment text lists create, edit, delete, update, search, sort and favorite; search covers name, email and phone instead of tags.
- **No pagination.** The list endpoint returns all matching contacts.
- **First and last name are required** (marked with `*` in the mockup's form). Email is optional but must be valid if given. Phone is free text because formats vary by country.
- **Search** is a case-insensitive substring match. It also matches the full name, so `alan t` finds Alan Turing.
- **IDs are never reused.** After a contact is deleted, its id is not given to a new contact.
- **Data is not persistent.** All data lives in memory, as the assignment requires, and is lost when the app restarts. Six sample contacts are loaded at startup so the API can be tried right away. On free hosting tiers the app may sleep when idle, which also resets the data back to the sample contacts.
- `created_at` can be used for sorting but is not included in responses.

## Issues encountered

- **`204` with a response body.** Declaring `response_model=bool` together with `status_code=204` on the DELETE route made FastAPI refuse to start (`AssertionError: Status code 204 must not have a response body`). Removing the response model fixed it.
- **PATCH and `null` values.** The first PATCH schema typed `first_name` as `str | None`. That allowed `{"first_name": null}`, which saved `None` into a required field; every later request that returned that contact then failed with `500`. The fix was to make the field optional but not nullable (`str = Field(default=None, ...)`), so a missing field is ignored and an explicit `null` gets `422`. The same rule was applied to `is_favorite`. `email` and `phone` stay nullable on purpose, so they can be cleared.
- **Combining filters.** An early version returned as soon as one filter matched, so `?search=...&favorite=true` ignored one of the two filters. The fix was to start from the full list and narrow it step by step, with a single `return` at the end.
- **Errors only at runtime.** Python has no compile step, so a leftover reference to a deleted variable only failed (`NameError`, `500`) when that endpoint was called. Each change was tested through Swagger and HTTP requests, and the VS Code Problems panel (Pylance) was used to catch this kind of mistake before running the code.
- **Hidden dependency.** Pydantic's `EmailStr` needs the separate `email-validator` package, so it is listed explicitly in `requirements.txt`.
- **Render URL blocked on some networks.** After deployment the service was live, but on a home internet connection every request to `*.onrender.com` failed during the TLS handshake (connection reset), while `render.com` itself loaded fine. Connecting to the same server IP with a different host name worked, which showed the block was based on the domain name, not a problem with the app. The same URL worked over mobile data.
- **Render settings.** The Root Directory field was first set to `app/`. That would have broken both the build (`requirements.txt` is in the repository root) and the start command (`uvicorn app.main:app` must run from the folder that contains `app/`), so it was left empty. The start command uses `--host 0.0.0.0` so the server accepts outside connections, and `--port $PORT` because Render chooses the port through the `PORT` environment variable.

## Running locally

Requires Python 3.10 or later (developed and tested on 3.14).

```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open http://127.0.0.1:8000/docs.

## Tech stack

- Python 3.14
- FastAPI (routing, OpenAPI/Swagger generation)
- Pydantic (request validation and serialization)
- Uvicorn (ASGI server)
