package com.csc195.pizza_final

import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.CheckBox
import android.widget.RadioButton
import android.widget.RadioGroup
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FirebaseFirestore

class MainActivity : AppCompatActivity() {

    // Declare UI elements for pizza size, toppings, cheese, sauce, and total price display
    lateinit var smallPizzaRadio: RadioButton
    lateinit var mediumPizzaRadio: RadioButton
    lateinit var largePizzaRadio: RadioButton
    lateinit var onionsCheckBox: CheckBox
    lateinit var olivesCheckBox: CheckBox
    lateinit var jalapenosCheckBox: CheckBox
    lateinit var pepperoniCheckBox: CheckBox
    lateinit var salamiCheckBox: CheckBox
    lateinit var sausageCheckBox: CheckBox
    lateinit var mozzarellaRadio: RadioButton
    lateinit var cheddarRadio: RadioButton
    lateinit var marinaraRadio: RadioButton
    lateinit var pestoRadio: RadioButton
    lateinit var totalPriceTextView: TextView
    lateinit var pizzaSizeRadioGroup: RadioGroup
    lateinit var cheeseRadioGroup: RadioGroup
    lateinit var sauceRadioGroup: RadioGroup

    // Firebase Auth instance for user authentication
    private lateinit var auth: FirebaseAuth
    // Firestore instance for saving orders
    private val db = FirebaseFirestore.getInstance()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // Initialize the UI components by linking to their XML IDs
        smallPizzaRadio = findViewById(R.id.smallpizza)
        mediumPizzaRadio = findViewById(R.id.mediumpizza)
        largePizzaRadio = findViewById(R.id.largepizza)
        onionsCheckBox = findViewById(R.id.OnionsCheckBox)
        olivesCheckBox = findViewById(R.id.OlivesCheckBox)
        jalapenosCheckBox = findViewById(R.id.JalapenosCheckBox)
        pepperoniCheckBox = findViewById(R.id.PepperoniCheckBox)
        salamiCheckBox = findViewById(R.id.SalamiCheckBox)
        sausageCheckBox = findViewById(R.id.SausageCheckBox)
        mozzarellaRadio = findViewById(R.id.MozzarellaRadioBtn)
        cheddarRadio = findViewById(R.id.CheddarRadioBtn)
        marinaraRadio = findViewById(R.id.MarinaraRadioBtn)
        pestoRadio = findViewById(R.id.PestoRadioBtn)
        totalPriceTextView = findViewById(R.id.Totalprice)
        pizzaSizeRadioGroup = findViewById(R.id.PizzaSizeRadio)
        cheeseRadioGroup = findViewById(R.id.CheeseRadioGroup)
        sauceRadioGroup = findViewById(R.id.SauceRadioGroup)

        // Initialize Firebase Auth for user authentication
        auth = FirebaseAuth.getInstance()

        // Check if the user is already signed in; if not, redirect to SignInActivity
        if (auth.currentUser == null) {
            // Redirect to the SignInActivity if the user is not signed in
            val signInIntent = Intent(this, SignInActivity::class.java)
            startActivity(signInIntent)
            finish() // Finish MainActivity to prevent it from being displayed behind the sign-in screen
        } else {
            Log.d("MainActivity", "User already signed in: ${auth.currentUser?.email}")
            enableUI() // Enable UI elements if the user is signed in
        }

        // Set up the "Place Your Order" button logic
        findViewById<View>(R.id.orderbutton).setOnClickListener {
            onPlaceOrderButtonClicked(it)
        }

        // Set up the "Sign Out" button logic
        findViewById<View>(R.id.signOutButton).setOnClickListener {
            onSignOutButtonClicked(it)
        }
    }

    // Enable all UI elements once the user is signed in
    private fun enableUI() {
        smallPizzaRadio.isEnabled = true
        mediumPizzaRadio.isEnabled = true
        largePizzaRadio.isEnabled = true
        onionsCheckBox.isEnabled = true
        olivesCheckBox.isEnabled = true
        jalapenosCheckBox.isEnabled = true
        pepperoniCheckBox.isEnabled = true
        salamiCheckBox.isEnabled = true
        sausageCheckBox.isEnabled = true
        mozzarellaRadio.isEnabled = true
        cheddarRadio.isEnabled = true
        marinaraRadio.isEnabled = true
        pestoRadio.isEnabled = true
        totalPriceTextView.isEnabled = true
        pizzaSizeRadioGroup.isEnabled = true
        cheeseRadioGroup.isEnabled = true
        sauceRadioGroup.isEnabled = true
    }

    // This function is called when the "Place Your Order" button is clicked
    private fun onPlaceOrderButtonClicked(view: View) {
        // Check if the user is authenticated
        if (auth.currentUser == null) {
            Toast.makeText(this, "Please wait until authenticated.", Toast.LENGTH_SHORT).show()
            return
        }

        // Calculate the price based on selected pizza size
        val pizzaSizePrice = when {
            smallPizzaRadio.isChecked -> 5.0
            mediumPizzaRadio.isChecked -> 7.0
            largePizzaRadio.isChecked -> 9.0
            else -> 0.0
        }

        // Calculate the price based on selected cheese type
        val cheesePrice = when {
            mozzarellaRadio.isChecked -> 1.0
            cheddarRadio.isChecked -> 1.5
            else -> 0.0
        }

        // Calculate the price based on selected sauce type
        val saucePrice = when {
            marinaraRadio.isChecked -> 1.0
            pestoRadio.isChecked -> 1.5
            else -> 0.0
        }

        // Collect selected toppings and calculate additional cost
        val toppings = mutableListOf<String>().apply {
            if (onionsCheckBox.isChecked) add("onions")
            if (olivesCheckBox.isChecked) add("olives")
            if (jalapenosCheckBox.isChecked) add("jalapenos")
            if (pepperoniCheckBox.isChecked) add("pepperoni")
            if (salamiCheckBox.isChecked) add("salami")
            if (sausageCheckBox.isChecked) add("sausage")
        }

        // Calculate total price based on all selections
        val totalPrice = pizzaSizePrice + cheesePrice + saucePrice + toppings.size * 1.0 // Assuming each topping costs $1.0
        totalPriceTextView.text = "Total Order Price = $${totalPrice}"

        // Create an order map to save in Firestore
        val order = hashMapOf(
            "size" to getPizzaSize(),
            "cheese" to getCheeseType(),
            "sauce" to getSauceType(),
            "toppings" to toppings,
            "totalPrice" to totalPrice
        )

        // Save the order to Firestore with the current user's UID as the document ID
        db.collection("orders")
            .document(auth.currentUser!!.uid)
            .set(order)
            .addOnSuccessListener {
                Toast.makeText(this, "Order placed successfully!", Toast.LENGTH_SHORT).show()
            }
            .addOnFailureListener { e ->
                Log.w("MainActivity", "Error placing order", e)
                Toast.makeText(this, "Failed to place order.", Toast.LENGTH_SHORT).show()
            }
    }

    // Get pizza size
    private fun getPizzaSize(): String {
        return when {
            smallPizzaRadio.isChecked -> "Small"
            mediumPizzaRadio.isChecked -> "Medium"
            largePizzaRadio.isChecked -> "Large"
            else -> "None"
        }
    }

    // Get cheese type
    private fun getCheeseType(): String {
        return when {
            mozzarellaRadio.isChecked -> "Mozzarella"
            cheddarRadio.isChecked -> "Cheddar"
            else -> "None"
        }
    }

    // Get sauce type
    private fun getSauceType(): String {
        return when {
            marinaraRadio.isChecked -> "Marinara"
            pestoRadio.isChecked -> "Pesto"
            else -> "None"
        }
    }

    // This function is called when the "Sign Out" button is clicked
    private fun onSignOutButtonClicked(view: View) {
        auth.signOut()
        Toast.makeText(this, "Signed out successfully.", Toast.LENGTH_SHORT).show()

        // Redirect to the SignInActivity after sign-out
        val signInIntent = Intent(this, SignInActivity::class.java)
        startActivity(signInIntent)
        finish() // Close MainActivity
    }
}
