package com.example.calculator

import android.content.Context
import android.util.Log
import java.io.BufferedReader
import java.io.InputStreamReader

object TokenUtil {
    fun getUsername(context: Context): String {
        context.assets.open("user.txt").use { inputStream ->
            BufferedReader(InputStreamReader(inputStream, Charsets.UTF_8)).use { reader ->
                val username = reader.readText().trim()  // Remove any extra whitespace or newlines
                Log.d("TokenUtil", "Username read: $username")  // Log the username for verification
                return username
            }
        }
    }

    fun getPassword(context: Context): String {
        context.assets.open("pw.txt").use { inputStream ->
            BufferedReader(InputStreamReader(inputStream, Charsets.UTF_8)).use { reader ->
                val password = reader.readText().trim()  // Remove any extra whitespace or newlines
                Log.d("TokenUtil", "Password read: $password")  // Log the password for verification
                return password
            }
        }
    }
}
