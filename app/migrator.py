import os
import yaml
from sqlalchemy import text
from DB.models import MigrationLog
from DB import db

def run_migrations():
    # Получаем путь к файлу changelog.yaml
    current_dir = os.path.dirname(os.path.abspath(__file__))
    changelog_path = os.path.join(current_dir, 'scripts_migration', 'changelog.yaml')

    # Пытаемся открыть файл changelog.yaml
    try:
        with open(changelog_path) as file:
            # Загружаем содержимое файла в переменную changelog
            changelog = yaml.safe_load(file)
    except FileNotFoundError:
        # Обработка ошибки, если файл не найден
        print(f"Файл {changelog_path} не найден.")
        return
    except Exception as e:
        # Обработка других возможных ошибок при открытии файла
        print(f"Ошибка при открытии файла {changelog_path}: {e}")
        return

    # Получаем список выполненных миграций из базы данных
    executed_migrations = {m.migration_id for m in MigrationLog.query.all()}
    # Получаем список миграций из changelog
    changelog_migrations = {migration['id'] for migration in changelog}

    # Проверка на несоответствия между выполненными миграциями и записями в changelog
    if executed_migrations != changelog_migrations:
        print("Несоответствие между выполненными миграциями и changelog:")
        print(f"Выполненные миграции: {executed_migrations}")
        print(f"Миграции в changelog: {changelog_migrations}")
        raise Exception("База данных находится в несогласованном состоянии.")
    
    # Проходим по каждой миграции из changelog
    for migration in changelog:
        migration_id = migration['id']
        print(f"Проверка миграции: {migration_id}")
        
        # Если миграция еще не была выполнена, применяем ее
        if migration_id not in executed_migrations:
            try:
                apply_migration(migration['file_path'])  # Применяем миграцию
                log_migration(migration_id)  # Записываем миграцию в лог
                print(f"Миграция {migration_id} успешно применена.")
            except Exception as e:
                # Обработка ошибки, если не удалось применить миграцию
                print(f"Не удалось применить миграцию {migration_id}: {e}")

def apply_migration(file_path):
    # Импортируем приложение для использования контекста приложения
    from app.app import app
    
    # Создаем контекст приложения для выполнения миграции
    with app.app_context():
        try:
            # Открываем файл с SQL-скриптом миграции
            with open(file_path, 'r') as file:
                sql_script = file.read()  # Читаем содержимое файла
                print(f"Применение миграции: {file_path}")  
                db.session.execute(text(sql_script))  # Выполняем SQL-скрипт
                db.session.commit()  # Подтверждаем изменения в базе данных
                print(f"Миграция {file_path} успешно применена.")
        except Exception as e:
            db.session.rollback()  # Откатываем изменения в случае ошибки
            print(f"Ошибка при применении миграции {file_path}: {e}")

def log_migration(migration_id):
    # Импортируем объект базы данных для записи лога миграций
    from app.app import db
    
    new_log = MigrationLog(migration_id=migration_id)  # Создаем новый объект логирования миграции
    db.session.add(new_log)  # Добавляем запись в сессию базы данных
    
    try:
        db.session.commit()  # Подтверждаем запись в лог миграции
        print(f"Миграция {migration_id} записана в лог.")
    except Exception as e:
        db.session.rollback()  # Откатываем изменения в случае ошибки
        print(f"Ошибка при записи миграции {migration_id} в лог: {e}")
    