from flask import Blueprint, render_template, request, redirect, url_for
from DB import db
from DB.models import Subscriptions  # Убедитесь, что импортируете модель Subscription

# Создаем экземпляр класса Blueprint
rgr = Blueprint("rgr", __name__)


@rgr.route('/')
@rgr.route('/index')
def index():
    return render_template('index.html')


@rgr.route('/get_subscriptions', methods=['GET'])
def get_subscriptions():
    subscriptions = Subscriptions.query.all()
    return render_template("get_subscriptions.html", subscriptions=subscriptions)


@rgr.route('/create_subscriptions', methods=['GET', 'POST'])
def create_subscriptions():
    if request.method == 'POST':
        name = request.form.get('name')
        amount = request.form.get('amount')
        periodicity = request.form.get('periodicity')
        start_date = request.form.get('start_date')

        subscriptions = Subscriptions(name=name, amount=amount, periodicity=periodicity, start_date=start_date)
        db.session.add(subscriptions)
        db.session.commit()
        
        return redirect(url_for('rgr.get_subscriptions'))

    return render_template("create_subscriptions.html")


@rgr.route('/subscriptions/<int:id>', methods=['GET', 'POST'])
def update_subscriptions(id):
    subscriptions = Subscriptions.query.get_or_404(id)
    
    if request.method == 'POST':
        subscriptions.amount = request.form.get('amount', subscriptions.amount)
        subscriptions.periodicity = request.form.get('periodicity', subscriptions.periodicity)
        subscriptions.start_date = request.form.get('start_date', subscriptions.start_date)
        
        db.session.commit()
        return redirect(url_for('rgr.get_subscriptions')) 

    return render_template("update_subscriptions.html", subscriptions=subscriptions)

    
@rgr.route('/subscriptions/<int:id>/delete', methods=['POST'])
def delete_subscriptions(id):
    subscription = Subscriptions.query.get(id)
    db.session.delete(subscription)
    db.session.commit()
    return redirect(url_for('rgr.get_subscriptions')) 
