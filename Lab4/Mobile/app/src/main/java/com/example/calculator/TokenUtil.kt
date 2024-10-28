package com.example.calculator

import android.content.Context
import java.io.BufferedReader
import java.io.InputStreamReader

object TokenUtil {
    fun getAccessToken(context: Context): String {
        return context.assets.open("auth_token.txt").bufferedReader().use { it.readText().trim() }
    }

    fun getCredentials(context: Context): Pair<String, String> {
        val inputStream = context.assets.open("credentials.txt")
        val bufferedReader = BufferedReader(InputStreamReader(inputStream))
        val credentials = bufferedReader.use { it.readLines() }
        val username = credentials.find { it.startsWith("username=") }?.split("=")?.get(1) ?: ""
        val password = credentials.find { it.startsWith("password=") }?.split("=")?.get(1) ?: ""
        return Pair(username, password)
    }
}