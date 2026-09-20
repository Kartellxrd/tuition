# Android build path

This is a React Native JavaScript application.

Before a release build:
1. Set the real HTTPS production API in src/config.js.
2. Install dependencies.
3. Ensure Android SDK/JDK requirements pass the React Native doctor command.
4. Configure a release signing keystore outside Git.
5. Build the release APK/AAB with Gradle.

Never commit a keystore, signing password, Supabase service key, database password, JWT secret, or Resend API key.
