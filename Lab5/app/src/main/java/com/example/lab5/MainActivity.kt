package com.example.lab5

import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.CheckBox
import android.widget.RadioButton
import android.widget.RadioGroup
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {
    // Declare variables for UI elements
    lateinit var smallPizzaRadio: RadioButton
    lateinit var mediumPizzaRadio: RadioButton
    lateinit var largePizzaRadio: RadioButton
    lateinit var onionsCheckBox: CheckBox
    lateinit var olivesCheckBox: CheckBox
    lateinit var jalapenosCheckBox: CheckBox // renamed
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

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // Initialize the views using findViewById
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
    }

    // This function is called when the "Place Your Order" button is clicked
    fun onPlaceOrderButtonClicked(view: View) {
        Log.d("MainActivity", "Button Clicked")

        var pizzaSizePrice = 0.0
        var toppingsTotal = 0.0
        var cheesePrice = 0.0
        var saucePrice = 0.0

        // Check which pizza size was selected
        when {
            smallPizzaRadio.isChecked -> pizzaSizePrice = 5.0
            mediumPizzaRadio.isChecked -> pizzaSizePrice = 7.0
            largePizzaRadio.isChecked -> pizzaSizePrice = 9.0
        }

        // Check which cheese was selected
        if (mozzarellaRadio.isChecked) {
            cheesePrice = 1.0
        } else if (cheddarRadio.isChecked) {
            cheesePrice = 1.5
        }

        // Check which sauce was selected
        if (marinaraRadio.isChecked) {
            saucePrice = 1.0
        } else if (pestoRadio.isChecked) {
            saucePrice = 1.5
        }

        // Check which toppings were selected
        if (onionsCheckBox.isChecked) {
            toppingsTotal += 1.0
        }
        if (olivesCheckBox.isChecked) {
            toppingsTotal += 2.0
        }
        if (jalapenosCheckBox.isChecked) {
            toppingsTotal += 1.0
        }
        if (pepperoniCheckBox.isChecked) {
            toppingsTotal += 2.5
        }
        if (salamiCheckBox.isChecked) {
            toppingsTotal += 3.0
        }
        if (sausageCheckBox.isChecked) {
            toppingsTotal += 3.5
        }

        // Calculate and display the total order price
        val totalPrice = pizzaSizePrice + toppingsTotal + cheesePrice + saucePrice
        Log.d("MainActivity", "$$totalPrice")

        totalPriceTextView.text = "Total Order Price = $${totalPrice}"
    }
}
