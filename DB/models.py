from . import db  # Импортируем объект базы данных из текущего пакета

class Subscriptions(db.Model):  # Определяем модель подписок, наследующую от db.Model
    __tablename__ = 'subscriptions'  # Указываем имя таблицы в базе данных

    id = db.Column(db.Integer, primary_key=True)  # Определяем поле id как первичный ключ (целое число)
    name = db.Column(db.String(100), nullable=False)  # Определяем поле name как строку длиной до 100 символов, не допускающую значение NULL
    amount = db.Column(db.Float, nullable=False)  # Определяем поле amount как число с плавающей запятой, не допускающее значение NULL
    periodicity = db.Column(db.String(50), nullable=False)  # Определяем поле periodicity как строку длиной до 50 символов, не допускающую значение NULL
    start_date = db.Column(db.Date, nullable=False)  # Определяем поле start_date как дату, не допускающую значение NULL

class MigrationLog(db.Model):  # Определяем модель журнала миграций, наследующую от db.Model
    __tablename__ = 'migration_log'  # Указываем имя таблицы в базе данных

    id = db.Column(db.Integer, primary_key=True)  # Определяем поле id как первичный ключ (целое число)
    migration_id = db.Column(db.Integer, nullable=False)  # Определяем поле migration_id как целое число, не допускающее значение NULL