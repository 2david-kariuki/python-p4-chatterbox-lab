from app import app, db
from models import Message
from datetime import datetime

with app.app_context():
    db.session.query(Message).delete()
    messages = [
        Message(
            body='Hello, World!',
            username='Alice',
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        ),
        Message(
            body='How are you?',
            username='Bob',
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
    ]
    db.session.add_all(messages)
    db.session.commit()
    print('Database seeded with sample messages!')