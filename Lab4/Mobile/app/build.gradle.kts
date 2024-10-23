plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
}

android {
    namespace = "com.example.calculator"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.example.calculator"
        minSdk = 24
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
        vectorDrawables {
            useSupportLibrary = true
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_1_8
        targetCompatibility = JavaVersion.VERSION_1_8
    }
    kotlinOptions {
        jvmTarget = "1.8"
    }
    buildFeatures {
        compose = true
    }
    composeOptions {
        kotlinCompilerExtensionVersion = "1.5.1"
    }
    packaging {
        resources {
            excludes += "/META-INF/{AL2.0,LGPL2.1}"
        }
    }
}

dependencies {
    implementation(libs.androidx.core.ktx)
    implementation(libs.androidx.lifecycle.runtime.ktx)
    implementation(libs.androidx.activity.compose)
    implementation(platform(libs.androidx.compose.bom))

    // Jetpack Compose UI
    implementation("androidx.compose.ui:ui:1.5.1")

    // Compose Material (for Material Design components)
    implementation("androidx.compose.material3:material3:1.1.0-alpha05")

    // Tooling for previews
    implementation("androidx.compose.ui:ui-tooling-preview:1.5.1")

    // Retrofit is a type-safe HTTP client for Android and Java.
    // It simplifies making HTTP requests to RESTful web services and converting the responses into Java objects.
    implementation("com.squareup.retrofit2:retrofit:2.9.0")

    // Gson is a library used to convert Java objects into JSON and vice versa.
    // This converter allows Retrofit to automatically convert the server's JSON response into Java objects (and vice versa for sending requests).
    implementation("com.squareup.retrofit2:converter-gson:2.9.0")


    // Compose UI Tooling for debugging
    debugImplementation("androidx.compose.ui:ui-tooling:1.5.1")

    // For unit testing Compose components
    androidTestImplementation("androidx.compose.ui:ui-test-junit4:1.5.1")



    // Additional test dependencies
    testImplementation(libs.junit)
    androidTestImplementation(libs.androidx.junit)
    androidTestImplementation(libs.androidx.espresso.core)
}
