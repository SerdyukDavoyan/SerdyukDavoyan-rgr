import os  # Импортируем модуль для работы с операционной системой
import yaml  # Импортируем модуль для работы с YAML-файлами
from sqlalchemy import text  # Импортируем функцию для работы с текстовыми SQL-запросами
from DB.models import MigrationLog  # Импортируем модель для записи логов миграций
from DB import db  # Импортируем объект базы данных

def run_migrations():
    # Получаем путь к файлу changelog.yaml
    current_dir = os.path.dirname(os.path.abspath(__file__))  # Получаем текущую директорию
    changelog_path = os.path.join(current_dir, 'scripts_migration', 'changelog.yaml')  # Формируем полный путь к файлу changelog.yaml

    try:
        with open(changelog_path) as file:  # Открываем файл changelog.yaml для чтения
            changelog = yaml.safe_load(file)  # Загружаем содержимое файла в переменную changelog
    except FileNotFoundError:  # Обработка ошибки, если файл не найден
        print(f"Файл {changelog_path} не найден.")  # Выводим сообщение об ошибке
        return  # Завершаем выполнение функции
    except Exception as e:  # Обработка других возможных ошибок
        print(f"Ошибка при открытии файла {changelog_path}: {e}")  # Выводим сообщение об ошибке
        return  # Завершаем выполнение функции

    # Получаем набор уже выполненных миграций из базы данных
    executed_migrations = {m.migration_id for m in MigrationLog.query.all()}

    for migration in changelog:  # Проходим по каждой миграции в changelog
        migration_id = migration['id']  # Извлекаем идентификатор миграции
        print(f"Проверка миграции: {migration_id}")  # Выводим информацию о проверке миграции
        if migration_id not in executed_migrations:  # Проверяем, была ли миграция уже выполнена
            try:
                apply_migration(migration['file_path'])  # Применяем миграцию по указанному пути
                log_migration(migration_id)  # Записываем миграцию в лог
                print(f"Миграция {migration_id} успешно применена.")  # Выводим сообщение об успешном применении миграции
            except Exception as e:  # Обработка ошибок при применении миграции
                print(f"Не удалось применить миграцию {migration_id}: {e}")  # Выводим сообщение об ошибке
        else:
            print(f"Миграция {migration_id} уже была применена.")  # Если миграция уже выполнена, выводим соответствующее сообщение


def apply_migration(file_path):
    from app.app import app  # Импортируем приложение Flask для контекста приложения
    with app.app_context():  # Создаем контекст приложения для выполнения операций с базой данных
        try:
            with open(file_path, 'r') as file:  # Открываем файл миграции для чтения
                sql_script = file.read()  # Читаем содержимое файла в переменную sql_script
                print(f"Применение миграции: {file_path}")  # Выводим информацию о применении миграции  
                db.session.execute(text(sql_script))  # Выполняем SQL-скрипт в сессии базы данных
                db.session.commit()  # Фиксируем изменения в базе данных
                print(f"Миграция {file_path} успешно применена.")  # Выводим сообщение об успешном применении миграции
        except Exception as e:  # Обработка ошибок при применении миграции
            db.session.rollback()  # Откатываем изменения в случае ошибки
            print(f"Ошибка при применении миграции {file_path}: {e}")  # Выводим сообщение об ошибке


def log_migration(migration_id):
    from app.app import db  # Импортируем объект базы данных
    new_log = MigrationLog(migration_id=migration_id)  # Создаем новый объект лога миграции
    db.session.add(new_log)  # Добавляем новый лог в сессию базы данных
    try:
        db.session.commit()  # Фиксируем изменения в базе данных
        print(f"Миграция {migration_id} записана в лог.")  # Выводим сообщение об успешной записи в лог
    except Exception as e:  # Обработка ошибок при записи в лог
        db.session.rollback()  # Откатываем изменения в случае ошибки
        print(f"Ошибка при записи миграции {migration_id} в лог: {e}")  # Выводим сообщение об ошибке