import unittest
from unittest.mock import patch, mock_open
from app.migrator import run_migrations

class TestMigrator(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data='- id: create_subscriptions_table\n  file_path: app/scripts_migration/create_subscriptions_table.sql')
    @patch('app.migrator.db.session')
    def test_run_migrations(self, mock_db_session, mock_open):
        # Задаем поведение Mock для логов миграций
        mock_db_session.execute.return_value = None
        mock_db_session.commit.return_value = None

        # Запускаем миграции
        run_migrations()

        # Проверяем, что функция commit была вызвана
        self.assertTrue(mock_db_session.commit.called)

if __name__ == '__main__':
    unittest.main()
