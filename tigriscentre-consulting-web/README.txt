Explanation of the Code
main.py: Sets up the FastAPI app and defines the OAuth2PasswordBearer with various scopes based on the roles (Admin, Consultant, Client). Each scope corresponds to a specific action or permission.

auth_utils.py: Implements the get_current_user function, which:

Decodes and verifies the JWT token.
Checks if the user has the required scopes (permissions) for the endpoint.
Raises an HTTPException if the token is invalid or the required scopes are missing.
endpoints.py: Defines API endpoints based on roles and scopes:

Each endpoint specifies the required scope in the Security dependency.
For example, only a user with the admin:analytics scope can access the /admin/analytics endpoint.
This setup ensures that:

Authentication: The JWT token is verified for authenticity.
Authorization: Only users with the required scopes can access specific endpoints, providing role-based access control.
This approach keeps the code modular and easy to maintain while enforcing least privilege access based on your permissions matrix. Let me know if you have further quest



1. Define OAuth2 Scopes for Each Role in FastAPI
Assign specific scopes to each role based on the privileges, access, and actions defined in your matrix. Here’s a suggestion for scopes:

Admin:
"admin:manage" - Full access to manage all consultants, clients, appointments, etc.
"admin:analytics" - Access to analytics and reporting.

Consultant:
"consultant:profile" - Manage own profile.
"consultant:availability" - Set and update own availability.
"consultant:appointments" - Manage own appointments.
"consultant:messages" - Send/receive messages with clients.

Client:
"client:browse_consultants" - Access to browse consultants.
"client:appointments" - Book, reschedule, and cancel own appointments.
"client:messages" - Message consultants they have booked.






############################### FIREBASE ###############################

users (collection)
└── user_id (document)
    ├── name: string
    ├── email: string
    ├── role: string ("admin", "consultant", "client")
    ├── profile_image: string (URL)
    ├── bio: string

appointments (collection)
└── appointment_id (document)
    ├── client_id: reference (to a user document)
    ├── consultant_id: reference (to a user document)
    ├── scheduled_time: timestamp
    ├── status: string ("scheduled", "completed", "canceled")
    ├── notes: string (optional, for any additional info)
    ├── created_at: timestamp


conversations (collection)
└── conversation_id (document)   # Could be a combination of user IDs, e.g., "clientId_consultantId"
    ├── participants: array (e.g., [client_id, consultant_id])
    ├── last_message: string
    ├── last_message_time: timestamp
    ├── messages (subcollection)
        └── message_id (document)
            ├── sender_id: reference (to a user document)
            ├── content: string
            ├── sent_at: timestamp


############################### FIREBASE RULES ###############################
rules_version = '2';

service cloud.firestore {
  match /databases/{database}/documents {

    // Only allow authenticated users to read and write
    match /{document=**} {
      allow read, write: if request.auth != null;
    }

    // Allow only users with a specific UID to access an "admin" collection
    match /admin/{documentId} {
      allow read, write: if request.auth.uid == "specific_admin_uid";
    }

    // Only allow users to access their own documents in "users" collection
    match /users/{userId} {
      allow read, write: if request.auth.uid == userId;
    }
  }
}


