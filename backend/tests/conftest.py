import os
os.environ.setdefault("DATABASE_URL","postgresql+psycopg2://user:pass@localhost/test")
os.environ.setdefault("JWT_SECRET","test-secret-that-is-long-enough-for-unit-tests-only")
os.environ.setdefault("SUPABASE_URL","https://example.supabase.co")
os.environ.setdefault("SUPABASE_SERVICE_ROLE_KEY","test-service-role-key")
