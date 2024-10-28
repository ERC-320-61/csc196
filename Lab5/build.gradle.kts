// Project-level build.gradle.kts

plugins {
    alias(libs.plugins.android.application) apply false
    alias(libs.plugins.kotlin.android) apply false

    // Add the Google services plugin for Firebase integration
    id("com.google.gms.google-services") version "4.4.2" apply false
}

// You don't need to add anything else for Firebase here.
