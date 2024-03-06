DO $$
BEGIN
    IF NOT EXISTS (
        SELECT FROM pg_database WHERE datname = 'origen'
    ) THEN
        CREATE DATABASE origen;
    END IF;
END
$$;