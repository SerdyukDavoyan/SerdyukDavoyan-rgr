-- app/scripts_migration/create_subscriptions_table.sql
CREATE TABLE IF NOT EXISTS subscriptions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    amount FLOAT NOT NULL,
    start_date DATE NOT NULL
);
