from flask import Blueprint, request, jsonify  # Импортируем необходимые модули из Flask
from DB import db  # Импортируем объект базы данных
from DB.models import Subscriptions  # Импортируем модель Subscription

# Создаем экземпляр класса Blueprint для организации маршрутов
rgr = Blueprint("rgr", __name__)

# Получение подписки
@rgr.route('/subscriptions', methods=['GET'])
def get_subscriptions():
    # Получаем все подписки из базы данных
    subscriptions = Subscriptions.query.all()
    
    # Возвращаем список подписок в формате JSON
    return jsonify([{
        'id': sub.id,
        'name': sub.name,
        'amount': sub.amount,
        'periodicity': sub.periodicity,
        'start_date': sub.start_date.strftime('%Y-%m-%d')  # Преобразуем дату в строку формата 'YYYY-MM-DD'
    } for sub in subscriptions]), 200  # Возвращаем статус 200 (OK)

# Создание новой подписки
@rgr.route('/subscriptions', methods=['POST'])
def create_subscription():
    # Получаем данные из запроса в формате JSON
    data = request.get_json()
    
    # Проверяем, что все необходимые поля присутствуют в данных
    if not all(key in data for key in ('name', 'amount', 'periodicity', 'start_date')):
        return jsonify({'error': 'Missing data'}), 400  # Возвращаем ошибку 400 (Bad Request) при отсутствии данных

    # Создаем новый объект подписки на основе полученных данных
    subscription = Subscriptions(
        name=data['name'],
        amount=data['amount'],
        periodicity=data['periodicity'],
        start_date=data['start_date']  # Предполагается, что формат даты корректен
    )
    
    # Добавляем новую подписку в сессию базы данных и сохраняем изменения
    db.session.add(subscription)
    db.session.commit()

    # Возвращаем ID созданной подписки с кодом статуса 201 (Created)
    return jsonify({'Subscription id ': subscription.id}), 201

# Обновление существующей подписки по ID
@rgr.route('/subscriptions/<int:id>', methods=['PUT'])
def update_subscription(id):
    # Получаем данные из запроса в формате JSON
    data = request.get_json()
    
    # Получаем подписку по ID, если не найдена — возвращаем ошибку 404 (Not Found)
    subscription = Subscriptions.query.get_or_404(id)

    # Обновляем поля подписки на основе полученных данных
    subscription.name = data['name']
    subscription.amount = data['amount']
    subscription.periodicity = data['periodicity']
    subscription.start_date = data['start_date']

    # Сохраняем изменения в базе данных
    db.session.commit()
    
    # Возвращаем сообщение об успешном обновлении с кодом статуса 200 (OK)
    return jsonify({'message': 'Subscription updated successfully'}), 200

# Удаление подписки по ID
@rgr.route('/subscriptions/<int:id>', methods=['DELETE'])
def delete_subscription(id):
    # Получаем подписку по ID, если не найдена — возвращаем ошибку 404 (Not Found)
    subscription = Subscriptions.query.get_or_404(id)
    
    db.session.delete(subscription)
    db.session.commit()
    
    return '', 204  # Возвращаем статус 204 