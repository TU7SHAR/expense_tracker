from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    from blueprints.auth import auth_bp
    from blueprints.dashboard import dashboard_bp
    from blueprints.transactions import transactions_bp
    from blueprints.reports import reports_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(transactions_bp)
    app.register_blueprint(reports_bp)

    with app.app_context():
        from models import User, Transaction, Category
        db.create_all()
        _seed_categories(app)

    return app


def _seed_categories(app):
    from models import Category
    if Category.query.count() == 0:
        default_categories = [
            Category(name='Food & Dining', icon='bi-cup-hot', color='#FF6384'),
            Category(name='Transportation', icon='bi-car-front', color='#36A2EB'),
            Category(name='Housing', icon='bi-house', color='#FFCE56'),
            Category(name='Utilities', icon='bi-lightning', color='#4BC0C0'),
            Category(name='Healthcare', icon='bi-heart-pulse', color='#9966FF'),
            Category(name='Entertainment', icon='bi-controller', color='#FF9F40'),
            Category(name='Shopping', icon='bi-bag', color='#C9CBCF'),
            Category(name='Education', icon='bi-book', color='#7BC8A4'),
            Category(name='Salary', icon='bi-cash-stack', color='#4CAF50'),
            Category(name='Freelance', icon='bi-laptop', color='#8BC34A'),
            Category(name='Investment', icon='bi-graph-up-arrow', color='#009688'),
            Category(name='Other Income', icon='bi-plus-circle', color='#607D8B'),
            Category(name='Other Expense', icon='bi-three-dots', color='#795548'),
        ]
        db.session.add_all(default_categories)
        db.session.commit()


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
