from flask import Flask
from app.rgr import rgr
from DB import db 
from app.migrator import run_migrations

app = Flask(__name__)

@rgr.before_app_request
def before_first_request():
    # Запускаем миграции только один раз при первом запросе
    if not hasattr(app, 'migrations_run'):
        run_migrations()
        app.migrations_run = True  # Устанавливаем флаг, чтобы избежать повторного выполнения

# Регистрация модуля Blueprint
app.register_blueprint(rgr)

# Настройки базы данных PostgreSQL
app.secret_key = "12345"
user_db = "PolinaZaikoRPP"
host_ip = "127.0.0.1"
host_port = "5432"
database_name = "RPP_LAB_5"
password = "12345"

# Подключение к базе данных
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user_db}:{password}@{host_ip}:{host_port}/{database_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Отключаем функцию отслеживания изменений объектов в SQLAlchemy
db.init_app(app)  # Инициализирует объект базы данных db с приложением Flask.

if __name__ == "__main__":
    app.run()