package com.example.lab5

import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
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

        // Perform anonymous sign-in
        signInAnonymously()
    }

    // Function to sign in the user anonymously
    private fun signInAnonymously() {
        auth.signInAnonymously()
            .addOnCompleteListener(this) { task ->
                if (task.isSuccessful) {
                    // Log success message if sign-in is successful
                    Log.d("MainActivity", "Anonymous sign-in successful")
                } else {
                    // Log failure message and show toast if sign-in fails
                    Log.w("MainActivity", "Anonymous sign-in failed", task.exception)
                    Toast.makeText(this, "Authentication failed.", Toast.LENGTH_SHORT).show()
                }
            }
    }

    // This function is called when the "Place Your Order" button is clicked
    fun onPlaceOrderButtonClicked(view: View) {
        // Check if the user is authenticated
        if (auth.currentUser == null) {
            Toast.makeText(this, "Please wait until authenticated.", Toast.LENGTH_SHORT).show()
            return
        }

        Log.d("MainActivity", "Button Clicked")

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
            "price" to totalPrice
        )

        // Add the order to the "orders" collection in Firestore
        db.collection("orders")
            .add(order)
            .addOnSuccessListener { documentReference ->
                // Log the document ID on successful save
                Log.d("MainActivity", "Order saved with ID: ${documentReference.id}")

                // Inflate the custom toast layout
                val inflater = LayoutInflater.from(this)
                val layout = inflater.inflate(R.layout.custom_toast, null)

                // Set the text for the toast message
                val toastText = layout.findViewById<TextView>(R.id.toast_text)
                toastText.text = "Order placed!"

                // Create and show the custom toast
                val toast = Toast(applicationContext)
                toast.duration = Toast.LENGTH_SHORT
                toast.view = layout
                toast.show()
            }
            .addOnFailureListener { e ->
                // Log error and show a failure toast if saving fails
                Log.w("MainActivity", "Error saving order", e)
                Toast.makeText(this, "Failed to place order.", Toast.LENGTH_SHORT).show()
            }
    }

    // Helper function to get the selected pizza size
    private fun getPizzaSize(): String {
        return when {
            smallPizzaRadio.isChecked -> "small"
            mediumPizzaRadio.isChecked -> "medium"
            largePizzaRadio.isChecked -> "large"
            else -> "unknown"
        }
    }

    // Helper function to get the selected cheese type
    private fun getCheeseType(): String {
        return when {
            mozzarellaRadio.isChecked -> "mozzarella"
            cheddarRadio.isChecked -> "cheddar"
            else -> "none"
        }
    }

    // Helper function to get the selected sauce type
    private fun getSauceType(): String {
        return when {
            marinaraRadio.isChecked -> "marinara"
            pestoRadio.isChecked -> "pesto"
            else -> "none"
        }
    }
}
