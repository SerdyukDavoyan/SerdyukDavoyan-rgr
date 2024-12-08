from . import db

class Subscriptions(db.Model):
    __tablename__ = 'subscriptions'  

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    periodicity = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date, nullable=False)

class MigrationLog(db.Model):
    __tablename__ = 'migration_log' 

    id = db.Column(db.Integer, primary_key=True)
    migration_id = db.Column(db.Integer, nullable=False)
