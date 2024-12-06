package com.csc195.pizza_final

import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.widget.Button
import android.widget.EditText
import android.widget.ImageButton
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.google.android.gms.auth.api.identity.BeginSignInRequest
import com.google.android.gms.auth.api.identity.Identity
import com.google.android.gms.auth.api.identity.SignInClient
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.auth.GoogleAuthProvider
import com.google.firebase.auth.FirebaseUser
import java.io.IOException

class SignInActivity : AppCompatActivity() {

    private lateinit var signInClient: SignInClient
    private lateinit var auth: FirebaseAuth // Firebase Authentication instance
    private val TAG = "SignInActivity"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_sign_in)

        // Initialize Firebase Auth
        auth = FirebaseAuth.getInstance()

        // Initialize the sign-in client for Google One Tap
        signInClient = Identity.getSignInClient(this)

        // Set up the Google sign-in button click listener
        val googleSignInButton = findViewById<ImageButton>(R.id.btn_sign_in_google)
        googleSignInButton.setOnClickListener {
            triggerGoogleOneTapSignIn()
        }

        // Set up the Microsoft sign-in button click listener (this is just a placeholder)
        val msSignInButton = findViewById<ImageButton>(R.id.btn_sign_in_ms)
        msSignInButton.setOnClickListener {
            triggerMicrosoftSignIn()
        }

        // Set up the email/password sign-in button click listener
        val signInButton = findViewById<Button>(R.id.btn_sign_in)
        signInButton.setOnClickListener {
            signInWithEmailPassword()
        }
    }

    // Check if user is signed in (non-null) and update UI accordingly.
    override fun onStart() {
        super.onStart()
        // Get the current user
        val currentUser = auth.currentUser
        updateUI(currentUser)
    }

    // Trigger Google One Tap Sign-In
    private fun triggerGoogleOneTapSignIn() {
        // Create the Google sign-in request
        val signInRequest = BeginSignInRequest.builder()
            .setGoogleIdTokenRequestOptions(
                BeginSignInRequest.GoogleIdTokenRequestOptions.builder()
                    .setSupported(true)
                    .setFilterByAuthorizedAccounts(false) // Allow new accounts
                    .setServerClientId(getString(R.string.your_web_client_id)) // Replace with your server's client ID
                    .build()
            )
            .build()

        // Begin Google sign-in process
        signInClient.beginSignIn(signInRequest)
            .addOnSuccessListener { result ->
                try {
                    // Use startIntentSenderForResult to start the sign-in activity with the PendingIntent
                    startIntentSenderForResult(
                        result.pendingIntent.intentSender, // IntentSender from PendingIntent
                        REQUEST_CODE_SIGN_IN, // Request code for identifying the sign-in result
                        null, // Optional: Intent for extras (can be null)
                        0, // Flags for the Intent (can be 0)
                        0, // Flags for the Intent (can be 0)
                        0  // Flags for the Intent (can be 0)
                    )
                } catch (e: IOException) {
                    // Handle any error that might occur when starting the intent
                    Log.e(TAG, "Error starting sign-in intent", e)
                    Toast.makeText(this, "Google Sign-In Failed", Toast.LENGTH_SHORT).show()
                }
            }
            .addOnFailureListener { exception ->
                // Handle failure to start sign-in flow
                Log.e(TAG, "Google One Tap Sign-In Failed", exception)
                Toast.makeText(this, "Sign-In Error: ${exception.localizedMessage}", Toast.LENGTH_SHORT).show()
            }
    }

    // Trigger Microsoft Sign-In (this is just a placeholder, needs MSAL SDK for actual sign-in)
    private fun triggerMicrosoftSignIn() {
        // Placeholder for Microsoft sign-in logic
        Toast.makeText(this, "Microsoft Sign-In Triggered", Toast.LENGTH_SHORT).show()
    }

    // Handle the result from Google sign-in
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)

        // Check if the request code matches the sign-in request
        if (requestCode == REQUEST_CODE_SIGN_IN) {
            // If Google sign-in intent data is available, proceed with authentication
            val googleCredential = signInClient.getSignInCredentialFromIntent(data)
            val idToken = googleCredential.googleIdToken

            // If the Google ID token is present, authenticate with Firebase
            if (idToken != null) {
                // Create Firebase credential using the Google ID token
                val firebaseCredential = GoogleAuthProvider.getCredential(idToken, null)

                // Sign in to Firebase with the Google credential
                auth.signInWithCredential(firebaseCredential)
                    .addOnCompleteListener(this) { task ->
                        if (task.isSuccessful) {
                            // Sign-in success
                            Log.d(TAG, "signInWithCredential:success")
                            val user = auth.currentUser
                            updateUI(user)
                        } else {
                            // Sign-in failure
                            Log.w(TAG, "signInWithCredential:failure", task.exception)
                            updateUI(null)
                        }
                    }
            } else {
                Log.d(TAG, "No ID token!")
            }
        }
    }

    // Sign in with Email and Password
    private fun signInWithEmailPassword() {
        val email = findViewById<EditText>(R.id.editTextEmail).text.toString()
        val password = findViewById<EditText>(R.id.editTextPassword).text.toString()

        if (email.isEmpty() || password.isEmpty()) {
            Toast.makeText(this, "Please enter email and password", Toast.LENGTH_SHORT).show()
            return
        }

        auth.signInWithEmailAndPassword(email, password)
            .addOnCompleteListener(this) { task ->
                if (task.isSuccessful) {
                    // Sign-in success
                    val user = auth.currentUser
                    updateUI(user)
                } else {
                    // Sign-in failure
                    Toast.makeText(this, "Authentication Failed: ${task.exception?.message}", Toast.LENGTH_SHORT).show()
                }
            }
    }

    // Update the UI with the user's information
    private fun updateUI(user: FirebaseUser?) {
        if (user != null) {
            // Proceed to the next screen or show user information
            Toast.makeText(this, "Welcome ${user.displayName}", Toast.LENGTH_SHORT).show()
            // Navigate to the next screen (MainActivity)
            navigateToMain()
        } else {
            // Show a message to the user
            Toast.makeText(this, "Authentication Failed", Toast.LENGTH_SHORT).show()
        }
    }

    // Navigate to MainActivity
    private fun navigateToMain() {
        val intent = Intent(this, MainActivity::class.java)
        startActivity(intent)  // Start MainActivity
        finish()  // Close SignInActivity to remove it from the stack
    }

    // Sign out the user
    private fun signOut() {
        auth.signOut()
        updateUI(null)
    }

    companion object {
        private const val REQUEST_CODE_SIGN_IN = 1
    }
}
