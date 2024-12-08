from flask import Flask
from app.rgr import rgr
from DB import db 


app = Flask(__name__)

# Регистрация модуля Blueprint
app.register_blueprint(rgr)

app.secret_key = "12345"
user_db = "PolinaZaikoRPP"
host_ip = "127.0.0.1"
host_port = "5432"
database_name = "RPP_LAB_5"
password = "12345"

# Подключение к базе данных
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user_db}:{password}@{host_ip}:{host_port}/{database_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
db.init_app(app)  

from app.migrator import run_migrations
# Запуск миграций перед запуском приложения
with app.app_context():
    print("Запуск миграций...")
    run_migrations()
