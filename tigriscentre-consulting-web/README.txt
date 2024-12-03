# Tigris Centre Consulting API

## Project Overview
The **Tigris Centre Consulting API** is a FastAPI-based application designed to manage users, consultants, appointments, and communications for a consulting service. The platform leverages Firebase Firestore as its database and implements role-based access control (RBAC) using OAuth2 scopes to ensure secure, modular, and maintainable code.

This project empowers admins, consultants, and clients to perform their respective tasks while enforcing authentication and least privilege access.

---

## Features

### 🔐 **Authentication and Authorization**
- **JWT Authentication:** Verifies and decodes tokens to validate user sessions.
- **Role-Based Access Control (RBAC):** Implements specific OAuth2 scopes to restrict access based on roles:
  - **Admin Scopes:**
    - `admin:manage` - Full administrative control.
    - `admin:analytics` - Access analytics and reporting.
  - **Consultant Scopes:**
    - `consultant:profile` - Manage profile.
    - `consultant:availability` - Set/update availability.
    - `consultant:appointments` - Manage appointments.
    - `consultant:messages` - Communicate with clients.
  - **Client Scopes:**
    - `client:browse_consultants` - Browse consultant profiles.
    - `client:appointments` - Book, reschedule, and cancel appointments.
    - `client:messages` - Message consultants.
  
### 🗄️ **Firestore Database Schema**
Firestore is used as the backend database with the following collections:

#### **1. Users**
Manages all user profiles, including admins, consultants, and clients.
```plaintext
users (collection)
└── user_id (document)
    ├── name: string
    ├── email: string
    ├── role: string ("admin", "consultant", "client")
    ├── profile_image: string (URL)
    ├── bio: string
```

#### **2. Appointments**
Tracks appointments between clients and consultants.
```plaintext
appointments (collection)
└── appointment_id (document)
    ├── client_id: reference (to a user document)
    ├── consultant_id: reference (to a user document)
    ├── scheduled_time: timestamp
    ├── status: string ("scheduled", "completed", "canceled")
    ├── notes: string (optional, for any additional info)
    ├── created_at: timestamp
```

#### **3. Conversations**
Facilitates messaging between clients and consultants.
```plaintext
conversations (collection)
└── conversation_id (document)
    ├── participants: array (e.g., [client_id, consultant_id])
    ├── last_message: string
    ├── last_message_time: timestamp
    ├── messages (subcollection)
        └── message_id (document)
            ├── sender_id: reference (to a user document)
            ├── content: string
            ├── sent_at: timestamp
```

---

## Code Breakdown

### 📜 **`main.py`**
- Entry point for the FastAPI application.
- Sets up the app, OAuth2PasswordBearer, and includes modular endpoints for:
  - Authentication (`/auth`)
  - Admin operations (`/admin`)
  - Consultant operations (`/consultant`)
  - Client operations (`/client`)
  - Shared/common utilities (`/common`)

### 🛠️ **`auth_utils.py`**
- Implements the `get_current_user` function to:
  - Decode and validate JWT tokens.
  - Verify if users have required OAuth2 scopes for endpoint access.
  - Enforce role-based access control.

### 🚪 **`endpoints`**
Defines modular API endpoints for each role:
- **Admin:** Full system management.
- **Consultant:** Manage profile, availability, and appointments.
- **Client:** Browse consultants, book appointments, and message consultants.
- **Common:** Shared utilities like health checks and database connection testing.

### 🔥 **`firebase_config.py`**
- Initializes the Firebase Admin SDK.
- Provides a Firestore client (`db`) for reading and writing to the database.

---

## Firebase Firestore Rules
Firestore rules ensure secure database access:
```plaintext
rules_version = '2';

service cloud.firestore {
  match /databases/{database}/documents {

    // Only authenticated users can read and write
    match /{document=**} {
      allow read, write: if request.auth != null;
    }

    // Admin-specific collection access
    match /admin/{documentId} {
      allow read, write: if request.auth.uid == "specific_admin_uid";
    }

    // Users can only access their own documents
    match /users/{userId} {
      allow read, write: if request.auth.uid == userId;
    }
  }
}
```

---

## Setup and Installation

### 🔧 **Prerequisites**
- Docker & Docker Compose
- Firebase Admin SDK credentials
- Python 3.10

### ⚙️ **Steps**
1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo/tigriscentre-consulting-web.git
   cd tigriscentre-consulting-web
   ```

2. Create a `.env` file:
   ```env
   FIREBASE_ADMIN_CREDENTIALS=/path/to/your/firebase_credentials.json
   FIRESTORE_EMULATOR_HOST=firestore_emulator:8080
   ```

3. Build and start the application:
   ```bash
   docker-compose up --build
   ```

4. Access the API:
   - Health check: [http://localhost:8000/](http://localhost:8000/)
   - Test Firestore connection: [http://localhost:8000/common/test-db](http://localhost:8000/common/test-db)

---

## Testing Firestore
The `/common/test-db` endpoint performs a write and read operation to validate database connectivity:
```python
@router.get("/test-db")
async def test_firestore():
    test_ref = db.collection("test_collection").document("test_doc")
    test_data = {"test_key": "test_value", "timestamp": datetime.utcnow().isoformat()}
    test_ref.set(test_data)
    fetched_data = test_ref.get().to_dict()
    return {"message": "DB Connection Successful", "data": fetched_data}
```

---

## Future Enhancements
- Add real-time messaging via Firestore listeners.
- Implement automated appointment reminders.
- Build a frontend dashboard for clients and consultants.

---

## Contributing
Pull requests are welcome. For significant changes, open an issue first to discuss your ideas.

---

## License
This project is licensed under the MIT License. See `LICENSE` for details.

---

Enjoy using the **Tigris Centre Consulting API**! 🚀