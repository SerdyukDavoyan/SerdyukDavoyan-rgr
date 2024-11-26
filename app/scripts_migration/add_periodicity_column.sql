-- app/scripts_migration/add_periodicity_column.sql
ALTER TABLE subscriptions ADD COLUMN periodicity VARCHAR(50);
