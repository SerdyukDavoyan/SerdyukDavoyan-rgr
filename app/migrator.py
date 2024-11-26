import os
import yaml
from sqlalchemy import text
from DB.models import MigrationLog
from DB import db

def run_migrations():
    # Получаем путь к файлу changelog.yaml
    current_dir = os.path.dirname(os.path.abspath(__file__))
    changelog_path = os.path.join(current_dir, 'changelog.yaml')

    # Проверяем наличие файла и загружаем его
    try:
        with open(changelog_path) as file:
            changelog = yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Файл {changelog_path} не найден.")
        return
    except Exception as e:
        print(f"Ошибка при открытии файла {changelog_path}: {e}")
        return

    # Получаем список уже выполненных миграций
    executed_migrations = {m.migration_id for m in MigrationLog.query.all()}

    for migration in changelog:
        migration_id = migration['id']
        if migration_id not in executed_migrations:
            try:
                apply_migration(migration['file_path'])
                log_migration(migration_id)
            except Exception as e:
                print(f"Не удалось применить миграцию {migration_id}: {e}")

def apply_migration(file_path):
    from app.app import app
    with app.app_context():
        try:
            with open(file_path, 'r') as file:
                sql_script = file.read()
                print(f"Применение миграции: {file_path}")  # Логируем имя файла
                db.session.execute(text(sql_script))
                db.session.commit()
                print(f"Миграция {file_path} успешно применена.")
        except Exception as e:
            db.session.rollback()
            print(f"Ошибка при применении миграции {file_path}: {e}")

def log_migration(migration_id):
    from app.app import db
    new_log = MigrationLog(migration_id=migration_id)
    db.session.add(new_log)
    db.session.commit()