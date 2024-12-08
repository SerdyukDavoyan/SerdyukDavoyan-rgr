from flask import Blueprint, request, jsonify
from DB import db
from DB.models import Subscriptions  # Убедитесь, что импортируете модель Subscription

# Создаем экземпляр класса Blueprint
rgr = Blueprint("rgr", __name__)

@rgr.route('/subscriptions', methods=['GET'])
def get_subscriptions():
    subscriptions = Subscriptions.query.all()
    return jsonify([{
        'id': sub.id,
        'name': sub.name,
        'amount': sub.amount,
        'periodicity': sub.periodicity,
        'start_date': sub.start_date.strftime('%Y-%m-%d')  # Преобразуем дату в строку
    } for sub in subscriptions]), 200

@rgr.route('/subscriptions', methods=['POST'])
def create_subscription():
    data = request.get_json()
    if not all(key in data for key in ('name', 'amount', 'periodicity', 'start_date')):
        return jsonify({'error': 'Missing data'}), 400

    subscription = Subscriptions(
        name=data['name'],
        amount=data['amount'],
        periodicity=data['periodicity'],
        start_date=data['start_date']  # Предполагается, что формат даты корректен
    )
    db.session.add(subscription)
    db.session.commit()

    return jsonify({'id': subscription.id}), 201


# Обновление существующей подписки
@rgr.route('/subscriptions/<int:id>', methods=['PUT'])
def update_subscription(id):
    data = request.get_json()
    subscription = Subscriptions.query.get_or_404(id)

    # Обновляем поля подписки
    subscription.name = data['name']
    subscription.amount = data['amount']
    subscription.periodicity = data['periodicity']
    subscription.start_date = data['start_date']

    db.session.commit()
    
    return jsonify({'message': 'Subscription updated successfully'}), 200


@rgr.route('/subscriptions/<int:id>', methods=['DELETE'])
def delete_subscription(id):
    subscription = Subscriptions.query.get_or_404(id)
    db.session.delete(subscription)
    db.session.commit()
    return jsonify({'message': 'Subscription deleted successfully'}), 204
