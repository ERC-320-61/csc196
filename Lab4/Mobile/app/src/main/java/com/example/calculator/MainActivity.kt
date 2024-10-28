package com.example.calculator

import android.os.Bundle
import android.util.Log
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.calculator.ui.theme.CalculatorTheme
import retrofit2.*
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.Body
import retrofit2.http.Header
import retrofit2.http.POST

// Data models
data class CalculationRequest(val num1: Double, val num2: Double, val operation: String)
data class CalculationResponse(val result: Double?, val error: String?)
data class TokenResponse(val access: String, val refresh: String)

// Retrofit interfaces
interface AuthApi {
    @POST("token/")
    fun getToken(@Body credentials: Map<String, String>): Call<TokenResponse>
}

interface CalculatorApi {
    @POST("calculator/")
    fun calculate(@Header("Authorization") token: String, @Body request: CalculationRequest): Call<CalculationResponse>
}

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Retrieve credentials using TokenUtil
        val (username, password) = TokenUtil.getCredentials(this)
        Log.d("MainActivity", "Using Username: $username")

        // Initialize Retrofit
        val retrofit = Retrofit.Builder()
            .baseUrl("http://52.36.44.47:8000/api/")
            .addConverterFactory(GsonConverterFactory.create())
            .build()

        val authService = retrofit.create(AuthApi::class.java)

        // Request the token
        authService.getToken(mapOf("username" to username, "password" to password))
            .enqueue(object : Callback<TokenResponse> {
                override fun onResponse(call: Call<TokenResponse>, response: Response<TokenResponse>) {
                    if (response.isSuccessful) {
                        val token = response.body()?.access
                        Log.d("MainActivity", "Token received: $token")

                        // Set UI content with the token
                        setContent {
                            CalculatorTheme {
                                Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                                    AdditionApp(modifier = Modifier.padding(innerPadding), token = token)
                                }
                            }
                        }
                    } else {
                        Log.e("MainActivity", "Failed to authenticate: ${response.errorBody()?.string()}")
                    }
                }

                override fun onFailure(call: Call<TokenResponse>, t: Throwable) {
                    Log.e("MainActivity", "Authentication error: ${t.message}")
                }
            })
    }
}

@Composable
fun AdditionApp(modifier: Modifier = Modifier, token: String?) {
    var num1 by remember { mutableStateOf("") }
    var num2 by remember { mutableStateOf("") }
    var operation by remember { mutableStateOf("add") } // Hardcoded to "add" for simplicity
    var result by remember { mutableStateOf<Double?>(null) }
    var error by remember { mutableStateOf<String?>(null) }
    var isLoading by remember { mutableStateOf(false) }

    val retrofit = Retrofit.Builder()
        .baseUrl("http://52.36.44.47:8000/api/")
        .addConverterFactory(GsonConverterFactory.create())
        .build()

    val apiService = retrofit.create(CalculatorApi::class.java)

    Column(
        modifier = modifier
            .fillMaxSize()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Top
    ) {
        Text(
            text = result?.toString() ?: "Enter numbers",
            fontSize = 30.sp,
            textAlign = TextAlign.Center
        )

        OutlinedTextField(
            value = num1,
            onValueChange = { num1 = it },
            label = { Text("Enter first number") },
            keyboardOptions = KeyboardOptions.Default.copy(keyboardType = KeyboardType.Number),
            modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp)
        )

        OutlinedTextField(
            value = num2,
            onValueChange = { num2 = it },
            label = { Text("Enter second number") },
            keyboardOptions = KeyboardOptions.Default.copy(keyboardType = KeyboardType.Number),
            modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp)
        )

        Button(
            onClick = {
                val number1 = num1.toDoubleOrNull()
                val number2 = num2.toDoubleOrNull()
                if (number1 != null && number2 != null && token != null) {
                    isLoading = true
                    error = null

                    val request = CalculationRequest(number1, number2, operation)
                    val authHeader = "Bearer $token"

                    val call = apiService.calculate(authHeader, request)
                    call.enqueue(object : Callback<CalculationResponse> {
                        override fun onResponse(call: Call<CalculationResponse>, response: Response<CalculationResponse>) {
                            isLoading = false
                            if (response.isSuccessful) {
                                val responseBody = response.body()
                                result = responseBody?.result
                                error = responseBody?.error
                            } else {
                                error = "Server Error: ${response.code()}"
                            }
                        }

                        override fun onFailure(call: Call<CalculationResponse>, t: Throwable) {
                            isLoading = false
                            error = "Request Failed: ${t.message ?: "Unknown error"}"
                        }
                    })
                } else {
                    error = "Invalid input or token missing"
                }
            },
            modifier = Modifier.padding(16.dp)
        ) {
            Text("Calculate")
        }

        if (isLoading) {
            CircularProgressIndicator()
        }

        error?.let {
            Text(text = it, color = MaterialTheme.colorScheme.error)
        }
    }
}
