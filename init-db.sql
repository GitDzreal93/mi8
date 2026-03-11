-- Create mi8 database if not exists
-- (Already created by POSTGRES_DB, but this ensures it exists)

-- Enable PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;

-- Create additional extensions that might be useful
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
