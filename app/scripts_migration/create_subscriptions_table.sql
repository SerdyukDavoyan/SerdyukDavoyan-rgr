-- app/scripts_migration/create_subscriptions_table.sql
CREATE TABLE subscriptions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    amount FLOAT NOT NULL,
    periodicity VARCHAR(50) NOT NULL,
    start_date DATE NOT NULL
);
