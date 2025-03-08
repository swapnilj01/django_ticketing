# 🎟️ Event Ticketing API (Django + Django REST Framework)

This project is a **Django REST API** for managing event ticketing. It allows users to **register, login (JWT-based), view events, attend/unattend events, and manage events (admin-only).**  

---

## 🚀 Features
- **User Authentication**: JWT-based login & registration with email.
- **Event Management**: Create, update, delete events (admin-only).
- **User Interaction**: Users can attend/unattend events and see attendees.
- **Discount System**: Female users get a 5% discount on event tickets.

---

## 🛠️ Tools & Technologies Used
- **Python 3.x**
- **Django** - Web framework
- **Django REST Framework (DRF)** - API framework
- **Django SimpleJWT** - JWT authentication
- **drf-yasg** - Swagger UI for API documentation
- **SQLite** (default) / PostgreSQL (recommended)

---

## 📌 Project Setup & Installation

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/your-username/event-ticketing-api.git
cd event-ticketing-api
```

### **2️⃣ Set Up Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # (Mac/Linux)
venv\Scripts\activate  # (Windows)
```

### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4️⃣ Apply Migrations, Create Superuser and Run server**
```bash
python manage.py migrate
python manage.py createsuperuser

python manage.py runserver
```


### **6️⃣ Access the API**
Swagger API Docs: http://127.0.0.1:8000/swagger/
ReDoc API Docs: http://127.0.0.1:8000/redoc/

## 📌 API Endpoints (Short Description)

### **🔹 Authentication**
| Method | Endpoint                  | Description |
|--------|---------------------------|-------------|
| `POST` | `/api/register/`          | Register a new user |
| `POST` | `/api/login/`             | Get JWT token (login) |
| `POST` | `/api/token/refresh/`     | Refresh JWT token |

### **🔹 Events**
| Method  | Endpoint                   | Description |
|---------|----------------------------|-------------|
| `GET`   | `/api/events/`             | List all events |
| `GET`   | `/api/events/{id}/`        | Get details of a single event |
| `POST`  | `/api/events/create/` 🔒  | **Admin-only** - Create event |
| `DELETE` | `/api/events/{id}/delete/` 🔒 | **Admin-only** - Delete event |

### **🔹 Event Attendance**
| Method  | Endpoint                     | Description |
|---------|------------------------------|-------------|
| `POST`  | `/api/events/{id}/attend/`   | User attends an event |
| `DELETE` | `/api/events/{id}/attend/`  | User unattends an event |
| `GET`   | `/api/events/{id}/attendees/` | Get list of attendees |

**🔒 = Admin-only actions**


## 🗄️ Database Schema Overview

### **1️⃣ User Model (`User`)**
| Field Name  | Type         | Description |
|-------------|-------------|-------------|
| `id`        | Integer (Auto) | Unique User ID (Primary Key) |
| `email`     | String (Unique) | User's email (used for login) |
| `password`  | String | Hashed password |
| `first_name` | String | First Name |
| `last_name` | String | Last Name |
| `gender`    | ChoiceField | `Male`, `Female`, `Other` |
| `is_staff`  | Boolean | Admin privileges (`True` for admin users) |
| `is_active` | Boolean | User account status (`True` if active) |

---

### **2️⃣ Event Model (`Event`)**
| Field Name      | Type         | Description |
|----------------|-------------|-------------|
| `id`           | Integer (Auto) | Unique Event ID (Primary Key) |
| `title`        | String | Event Title |
| `description`  | Text | Event Description |
| `date`        | DateTime | Event Date & Time |
| `ticket_price` | Float | Ticket price for the event |

---

### **3️⃣ Attendance Model (`EventAttendance`)**
| Field Name  | Type            | Description |
|-------------|----------------|-------------|
| `id`        | Integer (Auto) | Unique Attendance ID (Primary Key) |
| `user`      | ForeignKey (`User`) | User attending the event |
| `event`     | ForeignKey (`Event`) | Event being attended |

---

📌 **Notes:**
- The `User` model replaces Django’s default authentication system and uses `email` instead of `username` for login.
- The `EventAttendance` model is a **many-to-many relationship** between Users and Events, allowing users to **attend/unattend events**.
- The `is_staff` field in `User` determines **admin privileges**, restricting event creation and deletion to admins.

