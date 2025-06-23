from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Message
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatterbox.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = Message.query.order_by(Message.created_at.asc()).all()
        return jsonify([message.to_dict() for message in messages])
    elif request.method == 'POST':
        data = request.get_json()
        if not data.get('body') or not data.get('username'):
            return make_response(jsonify({'error': 'Body and username are required'}), 400)
        new_message = Message(
            body=data['body'],
            username=data['username'],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.session.add(new_message)
        db.session.commit()
        return jsonify(new_message.to_dict()), 201

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def message_by_id(id):
    message = Message.query.get_or_404(id)
    if request.method == 'PATCH':
        data = request.get_json()
        if not data.get('body'):
            return make_response(jsonify({'error': 'Body is required'}), 400)
        message.body = data['body']
        message.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify(message.to_dict())
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        return make_response('', 204)

if __name__ == '__main__':
    app.run(port=5000, debug=True)