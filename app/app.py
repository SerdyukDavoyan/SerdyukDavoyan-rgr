from flask import Flask  # Импортируем класс Flask для создания веб-приложения
from app.rgr import rgr  # Импортируем модуль rgr из приложения для регистрации в качестве Blueprint
from DB import db  # Импортируем объект db для работы с базой данных

app = Flask(__name__)  # Создаем экземпляр приложения Flask

# Регистрация модуля Blueprint для обработки маршрутов, определенных в rgr
app.register_blueprint(rgr)

# Установка секретного ключа для сессий и защиты 
app.secret_key = "12345"

# Настройки подключения к базе данных
user_db = "RPP"  # Имя пользователя базы данных
host_ip = "127.0.0.1"  # IP-адрес хоста базы данных 
host_port = "5432"  # Порт, на котором работает база данных PostgreSQL
database_name = "RPP_RGR"  # Имя базы данных
password = "12345"  # Пароль пользователя базы данных

# Конфигурация подключения к базе данных PostgreSQL с использованием SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user_db}:{password}@{host_ip}:{host_port}/{database_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Отключение отслеживания изменений объектов для повышения производительности

# Инициализация объекта db с приложением Flask
db.init_app(app)  

from app.migrator import run_migrations  # Импорт функции для выполнения миграций базы данных

# Запуск миграций перед запуском приложения
with app.app_context():  # Создание контекста приложения для выполнения миграций
    print("Запуск миграций...")  # Вывод сообщения о начале миграций
    run_migrations()  # Вызов функции для выполнения миграций базы данных
