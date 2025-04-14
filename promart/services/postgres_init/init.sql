<<<<<<< HEAD
=======
-- user service üçün baza artıq var: promart
-- indi product service üçün ayrıca baza və user yaradırıq

>>>>>>> 0fcf8c5f75a945c84a88977ec1336a8f80e94c41
CREATE DATABASE productdb;

CREATE USER productuser WITH PASSWORD 'secret123';

GRANT ALL PRIVILEGES ON DATABASE productdb TO productuser;