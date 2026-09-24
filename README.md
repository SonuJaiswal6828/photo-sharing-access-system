# 📸 PhotoShare — Secure Photo Sharing System

A full-stack photo sharing platform with **temporary access control**. Admins organize photos into groups and sections, then grant **1-hour temporary access** to friends. Access can be revoked anytime.

**Live Demo:** [Add your deployed URL if hosted]  
**Repository:** https://github.com/SonuJaiswal6828/photo-sharing-access-system

---

## 🎯 Project Overview

PhotoShare solves a simple problem: **How do you share photos securely, with time-limited access, and full control?**

Traditional sharing (WhatsApp, Google Drive) gives **permanent access**. PhotoShare gives **temporary access** — exactly 1 hour — and the admin can **revoke anytime**.

### Core Idea
- Admin creates **Groups** (e.g., "Wedding 2026") with a unique code + password
- Admin organizes photos into **Sections** within each group (e.g., "Haldi", "Reception")
- Friend requests access using the group code + password
- Admin **approves** → friend gets a **1-hour session token**
- Friend views/downloads photos until session expires or is revoked

---

## ✨ Features

### 👤 Admin
- 🔐 Signup & login with JWT authentication
- 🔒 Password hashing with bcrypt + salt
- 📁 Create / edit / delete **groups** (auto-generated group codes)
- 📂 Create / edit / delete **sections** within groups
- 🖼️ Upload photos to **Cloudinary** (signed upload)
- ✅ View all **pending access requests**
- ✔️ Approve or ❌ reject requests
- ⏱️ Manage active **sessions** (view + revoke)

### 👥 Friend (No Login Required)
- 🔓 Request access using group code + password
- 🔍 Check request status via request code
- 📸 View & download photos using session token
- ⏰ Session auto-expires after 1 hour

### 🔐 Security
- JWT-based authentication for admin routes
- bcrypt password hashing with salt
- **User enumeration protection** (same error for wrong username/password)
- 32-character random session tokens
- Ownership verification on every mutation
- Auto-expiry + manual revoke
- Expired request auto-cleanup
- CORS configured

---

## 🛠️ Tech Stack

### Backend
| Layer | Technology |
|---|---|
| Framework | FastAPI (Python) |
| Database | PostgreSQL |
| ORM | SQLAlchemy 2.0 |
| Auth | JWT (PyJWT) + bcrypt |
| Validation | Pydantic v2 |
| Image Storage | Cloudinary |
| Server | Uvicorn |

### Frontend
| Layer | Technology |
|---|---|
| Markup | HTML5 |
| Styling | Tailwind CSS (CDN) |
| Logic | Vanilla JavaScript |
| HTTP | Fetch API |
| Fonts | Inter (Google Fonts) |

---

## 📁 Project Structure
photo-sharing-access-system/
├── backend/
│ ├── admin/ # Admin auth (signup, login)
│ ├── groups/ # Group CRUD + sections listing
│ ├── sections/ # Section CRUD + photos listing
│ ├── photos/ # Cloudinary signature + save + delete
│ ├── access_requests/ # Request flow (create, approve, reject, status)
│ ├── sessions/ # Session management (status, revoke, list, photos)
│ ├── models/ # SQLAlchemy models
│ │ ├── admin.py
│ │ ├── group.py
│ │ ├── section.py
│ │ ├── photo.py
│ │ ├── access_request.py
│ │ └── session.py
│ ├── utils/
│ │ ├── security.py # hash_password, verify_password, JWT
│ │ ├── dependencies.py # get_current_admin
│ │ ├── code_generator.py # random codes
│ │ └── cloudinary_config.py
│ ├── database.py # DB connection
│ ├── create_tables.py # Table creation script
│ ├── main.py # FastAPI app + routers + CORS
│ ├── requirements.txt
│ └── .env # (not committed)
│
├── frontend/
│ ├── index.html # Home / Landing
│ ├── about.html # About + developer
│ ├── login.html # Admin login
│ ├── signup.html # Admin signup
│ ├── dashboard.html # Admin dashboard
│ ├── groups.html # Groups list + CRUD
│ ├── group-detail.html # Sections of a group
│ ├── section-detail.html # Photos + upload
│ ├── pending.html # Pending requests
│ ├── sessions.html # Active sessions
│ ├── request-access.html # Friend: request form
│ ├── request-status.html # Friend: status check
│ ├── session-photos.html # Friend: view photos
│ ├── css/
│ │ └── style.css
│ ├── js/
│ │ ├── api.js # API wrapper + auth helpers
│ │ ├── navbar.js # Dynamic navbar (role-based)
│ │ └── footer.js # Footer
│ └── public/
│ └── sonu.jpg
│
├── venv/ # Python virtual environment
├── .gitignore
└── README.md


---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.10+
- PostgreSQL
- Cloudinary account (free tier works)
- Modern web browser

### 1️⃣ Clone Repository
```bash
git clone https://github.com/SonuJaiswal6828/photo-sharing-access-system.git
cd photo-sharing-access-system

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\Activate.ps1

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
cd backend
pip install -r requirements.txt

DATABASE_URL=postgresql://username:password@localhost:5432/photoshare
JWT_SECRET_KEY=your-super-secret-key-here
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

cd backend
python create_tables.py

cd backend
uvicorn main:app --reload
Backend: http://127.0.0.1:8000
API Docs: http://127.0.0.1:8000/docs

cd frontend
python -m http.server 5500
Frontend: http://localhost:5500

📖 API Endpoints
🔐 Admin
Method	Endpoint	Description
POST	/admin/signup	Register admin
POST	/admin/login	Login (returns JWT)
📁 Groups
Method	Endpoint	Auth	Description
POST	/group/create	✅	Create group
GET	/group/	✅	List my groups
GET	/group/{id}/sections	✅	List group sections
PATCH	/group/{id}	✅	Edit group
DELETE	/group/{id}	✅	Delete group
📂 Sections
Method	Endpoint	Auth	Description
POST	/section/create	✅	Create section
PATCH	/section/{id}	✅	Edit section
DELETE	/section/{id}	✅	Delete section
GET	/section/{id}/photos	✅	List section photos
🖼️ Photos
Method	Endpoint	Auth	Description
GET	/photos/get-upload-signature	✅	Get Cloudinary signature
POST	/photos/save_photo	✅	Save photo URL to DB
DELETE	/photos/{id}	✅	Delete photo
🔓 Access Requests
Method	Endpoint	Auth	Description
POST	/access-request/create	❌	Friend requests access
GET	/access-request/pending	✅	List pending
PATCH	/access-request/{id}/approve	✅	Approve → creates session
PATCH	/access-request/{id}/reject	✅	Reject
GET	/access-request/status/{code}	❌	Friend checks status
⏱️ Sessions
Method	Endpoint	Auth	Description
GET	/session/all	✅	List all admin sessions
GET	/session/{id}/status	❌	Check session status
PATCH	/session/{id}/revoke	✅	Revoke session
GET	/session/{token}/photos	❌	View photos via token

Signup → Login → Dashboard
    ↓
Create Group (code + password auto-generated)
    ↓
Create Sections in group
    ↓
Upload Photos to sections (via Cloudinary)
    ↓
Review Pending Requests → Approve/Reject
    ↓
Manage Sessions → Revoke if needed

Enter group code + password → Request Access
    ↓
Get Request Code (e.g., "8419")
    ↓
Check Status periodically
    ↓
Once approved: receive session token
    ↓
View + Download Photos (valid for 1 hour)

🔒 Security Highlights
JWT Authentication — Admin routes protected

bcrypt Password Hashing — Never store plain passwords

User Enumeration Protection — Same error for wrong username OR password

Session Tokens — 32-char random, guess-resistant

Ownership Verification — Users can only modify their own data

Auto-expiry — Sessions expire after 1 hour

Manual Revoke — Admin can revoke anytime

CORS — Configured for cross-origin frontend

🎓 Learning Outcomes
This project demonstrates:

REST API design with FastAPI

SQLAlchemy ORM + relationships + JOINs

JWT authentication + middleware

Password hashing (bcrypt + salt)

Third-party integration (Cloudinary)

File upload flows (signed uploads)

Frontend-backend integration via Fetch API

Role-based UI rendering

Clean architecture (routers/controllers/schemas)

👨‍💻 Developer
Sonu Jaiswal
Full Stack Developer

📧 Email: sonuj6828@gmail.com

📱 Phone: 7776839491

📍 Location: Vasai East, Maharashtra, India

💻 GitHub: @SonuJaiswal6828

🌐 Portfolio: sonuj-portfolio.netlify.app

📝 License
This project is built for educational purposes as a college submission.

🙏 Acknowledgments
FastAPI

SQLAlchemy

Tailwind CSS

Cloudinary

PyJWT