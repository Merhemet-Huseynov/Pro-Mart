CREATE DATABASE productdb;

CREATE USER productuser WITH PASSWORD 'secret123';

GRANT ALL PRIVILEGES ON DATABASE productdb TO productuser;