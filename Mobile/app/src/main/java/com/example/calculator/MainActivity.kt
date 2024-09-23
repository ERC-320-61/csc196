package com.example.calculator

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*  // Provides layout components like Column, Row, etc.
import androidx.compose.foundation.text.KeyboardOptions // Used to specify keyboard type for input fields
import androidx.compose.material3.* // Material design components like Button, Text, OutlinedTextField
import androidx.compose.runtime.* // Required for state management in Compose
import androidx.compose.ui.Alignment // Helps align content inside a layout (like Center alignment)
import androidx.compose.ui.Modifier // Modifiers used to change appearance and layout behavior of UI elements
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType // Specifies the type of keyboard (e.g., Number, Text, etc.)
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview // Allows UI previews in Android Studio
import androidx.compose.ui.unit.dp // Used for defining dimensions (like padding, height, width) in density-independent pixels (dp)
import androidx.compose.ui.unit.sp
import com.example.calculator.ui.theme.CalculatorTheme // Custom theme for the app

// Main activity of the app
class MainActivity : ComponentActivity() {
    // This function is called when the activity is created
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // Set the UI content using Jetpack Compose
        setContent {
            // Apply the custom app theme
            CalculatorTheme {
                // Scaffold provides a structure for UI components (can include top bars, bottom bars, floating buttons, etc.)
                Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                    // Calling the composable function that holds the UI for the calculator
                    AdditionApp(modifier = Modifier.padding(innerPadding))
                }
            }
        }
    }
}

// Composable function representing the UI of the app
@Composable
fun AdditionApp(modifier: Modifier = Modifier) {
    // State variables to hold the values of the two numbers and the result
    var num1 by remember { mutableStateOf("") } // State for the first input number
    var num2 by remember { mutableStateOf("") } // State for the second input number
    var result by remember { mutableStateOf(0.0) } // State for the result of the addition

    // Column layout to stack UI components vertically
    Column(
        modifier = modifier
            .fillMaxSize() // Fill the entire screen size
            .padding(16.dp), // Add padding around the content
        horizontalAlignment = Alignment.CenterHorizontally, // Center the content horizontally
        verticalArrangement = Arrangement.Top // Center the content vertically
    ) {

        // Display result at the top with larger font size and bold weight
        Text(
            text = "$result",
            style = MaterialTheme.typography.bodyLarge.copy(
                fontSize = 64.sp, // Set font size to 64 sp
                fontWeight = FontWeight.Bold, // Set font weight to bold
                textAlign = TextAlign.Center // Center-align the text
            ),
            modifier = Modifier.fillMaxWidth().padding(vertical = 16.dp) // Center and space it out
        )

        Spacer(modifier = Modifier.height(16.dp)) // Add vertical space between the input fields

        // First input field for the user to enter the first number
        OutlinedTextField(
            value = num1, // The current value of the first number input
            onValueChange = { num1 = it }, // Update the first number state when the input changes
            label = { Text("Enter first number") }, // Label for the input field
            keyboardOptions = KeyboardOptions.Default.copy(keyboardType = KeyboardType.Number), // Ensure the number keyboard is displayed
            modifier = Modifier.fillMaxWidth() // Make the input field take the full width of the screen
        )

        Spacer(modifier = Modifier.height(16.dp)) // Add vertical space between the input fields

        // Second input field for the user to enter the second number
        OutlinedTextField(
            value = num2, // The current value of the second number input
            onValueChange = { num2 = it }, // Update the second number state when the input changes
            label = { Text("Enter second number") }, // Label for the input field
            keyboardOptions = KeyboardOptions.Default.copy(keyboardType = KeyboardType.Number), // Ensure the number keyboard is displayed
            modifier = Modifier.fillMaxWidth() // Make the input field take the full width of the screen
        )

        Spacer(modifier = Modifier.height(16.dp)) // Add vertical space before the button

        // Button to trigger the addition of the two numbers
        Button(
            onClick = {
                // Convert the input strings to numbers and calculate the result
                // If the input is empty or invalid, use 0.0 as the default value
                val number1 = num1.toDoubleOrNull() ?: 0.0
                val number2 = num2.toDoubleOrNull() ?: 0.0
                result = number1 + number2 // Perform the addition and update the result
            },
            modifier = Modifier.padding(16.dp) // Add padding around the button
        ) {
            // Text displayed on the button
            Text("Calculate Sum")
        }

    }
}

// Preview function to render the UI inside Android Studio's preview pane
@Preview(showBackground = true)
@Composable
fun AdditionAppPreview() {
    // Apply the app theme in the preview
    CalculatorTheme {
        // Display the AdditionApp UI in the preview
        AdditionApp()
    }
}
