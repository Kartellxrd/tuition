# Backend deployment

The FastAPI service is ready for Render configuration through the repository root render.yaml.

Required server-only environment values:
- DATABASE_URL
- JWT_SECRET
- SUPABASE_URL
- SUPABASE_SERVICE_ROLE_KEY

Never put these values in the React Native application.

After Render creates the service, verify:
- GET /api/v1/health
- GET /api/v1/health/database

Then replace the production placeholder in mobile/src/config.js with the real HTTPS Render API URL before making a release APK.

Email verification delivery remains intentionally unconfigured until a legitimate Resend sender/domain is available.
