-- user service üçün baza artıq var: promart
-- indi product service üçün ayrıca baza və user yaradırıq

CREATE DATABASE productdb;

CREATE USER productuser WITH PASSWORD 'secret123';

GRANT ALL PRIVILEGES ON DATABASE productdb TO productuser;