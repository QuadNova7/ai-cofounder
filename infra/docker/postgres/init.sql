-- Postgres Init Script
SELECT 'CREATE DATABASE aicofounder' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'aicofounder')\gexec
