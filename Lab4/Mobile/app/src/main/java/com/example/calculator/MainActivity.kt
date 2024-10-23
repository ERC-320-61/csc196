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
import retrofit2.*
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.Body
import retrofit2.http.POST

// Data model for the numbers to be added
data class Numbers(val number1: Int, val number2: Int)

// Data model for the result returned by the server
data class Result(val result: Int)

// Retrofit interface to interact with the server
interface AddNumbersApi {
    @POST("add")
    fun addNumbers(@Body numbers: Numbers): Call<Result>
}

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

@Composable
fun AdditionApp(modifier: Modifier = Modifier) {
    // State variables to hold the values of the two numbers and the result
    var num1 by remember { mutableStateOf("") }
    var num2 by remember { mutableStateOf("") }
    var result by remember { mutableStateOf<Double?>(null) }
    var error by remember { mutableStateOf<String?>(null) }
    var isLoading by remember { mutableStateOf(false) }

    // Retrofit setup
    val retrofit = Retrofit.Builder()
        .baseUrl("http://your-api-url.com/") // Replace with your actual base URL
        .addConverterFactory(GsonConverterFactory.create())
        .build()

    val apiService = retrofit.create(AddNumbersApi::class.java)

    // Column layout to stack UI components vertically
    Column(
        modifier = modifier
            .fillMaxSize()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Top
    ) {

        // Display result at the top with larger font size and bold weight
        Text(
            text = result?.toString() ?: "Enter numbers",
            style = MaterialTheme.typography.bodyLarge.copy(
                fontSize = 64.sp,
                fontWeight = FontWeight.Bold,
                textAlign = TextAlign.Center
            ),
            modifier = Modifier.fillMaxWidth().padding(vertical = 16.dp)
        )

        Spacer(modifier = Modifier.height(16.dp))

        // First input field for the user to enter the first number
        OutlinedTextField(
            value = num1,
            onValueChange = { num1 = it },
            label = { Text("Enter first number") },
            keyboardOptions = KeyboardOptions.Default.copy(keyboardType = KeyboardType.Number),
            modifier = Modifier.fillMaxWidth()
        )

        Spacer(modifier = Modifier.height(16.dp))

        // Second input field for the user to enter the second number
        OutlinedTextField(
            value = num2,
            onValueChange = { num2 = it },
            label = { Text("Enter second number") },
            keyboardOptions = KeyboardOptions.Default.copy(keyboardType = KeyboardType.Number),
            modifier = Modifier.fillMaxWidth()
        )

        Spacer(modifier = Modifier.height(16.dp))

        // Button to trigger the addition of the two numbers via API
        Button(
            onClick = {
                // Check if input is valid
                val number1 = num1.toIntOrNull()
                val number2 = num2.toIntOrNull()

                if (number1 != null && number2 != null) {
                    isLoading = true
                    error = null

                    // Make the API call
                    val call = apiService.addNumbers(Numbers(number1, number2))
                    call.enqueue(object : Callback<Result> {
                        override fun onResponse(call: Call<Result>, response: Response<Result>) {
                            isLoading = false
                            if (response.isSuccessful) {
                                result = response.body()?.result?.toDouble()
                            } else {
                                error = "Error: ${response.code()}"
                            }
                        }

                        override fun onFailure(call: Call<Result>, t: Throwable) {
                            isLoading = false
                            error = "Failed: ${t.message}"
                        }
                    })
                } else {
                    error = "Invalid input"
                }
            },
            modifier = Modifier.padding(16.dp)
        ) {
            Text("Calculate Sum")
        }

        // Show loading indicator if request is being made
        if (isLoading) {
            CircularProgressIndicator()
        }

        // Show error message if any
        error?.let {
            Text(text = it, color = MaterialTheme.colorScheme.error)
        }
    }
}

@Preview(showBackground = true)
@Composable
fun AdditionAppPreview() {
    CalculatorTheme {
        AdditionApp()
    }
}
