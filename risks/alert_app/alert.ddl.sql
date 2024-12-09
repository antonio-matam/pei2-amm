\connect postgres;
DROP DATABASE if exists db;
CREATE DATABASE db;
\connect db;

CREATE EXTENSION "uuid-ossp";
CREATE TABLE alerts (
    risk_id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    city_name varchar[80],
    risk text,
    level int
);

INSERT INTO alerts (risk, city_name, level) VALUES
    ('fire', 'Moscow', 1),
    ('fire', 'Alcalá de Henares', 2),
    ('snow', 'Torrejón', 3),
    ('radiation', 'Coslada', 8);
