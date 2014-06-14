# -*- coding: utf-8 -*-
from flask import Flask, redirect, render_template_string, request, url_for
from flask.ext.babel import Babel
from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.user import current_user, login_required, UserManager, UserMixin, SQLAlchemyAdapter
import datetime
import jwt

# Use a Class-based config to avoid needing a 2nd file
class ConfigClass(object):
    CSRF_ENABLED = True

    # Configure Flask-User
    USER_ENABLE_USERNAME         = True
    USER_ENABLE_CONFIRM_EMAIL    = True
    USER_ENABLE_CHANGE_USERNAME  = True
    USER_ENABLE_CHANGE_PASSWORD  = True
    USER_ENABLE_FORGOT_PASSWORD  = True
    USER_ENABLE_RETYPE_PASSWORD  = True
    USER_LOGIN_TEMPLATE = 'flask_user/login_or_register.html'
    USER_REGISTER_TEMPLATE = 'flask_user/login_or_register.html'

def create_app(test_config=None):                   # For automated tests
    # Setup Flask and read config from ConfigClass defined above
    app = Flask(__name__)
    app.config.from_object(__name__+'.ConfigClass')

    # Load local_settings.py if file exists         # For automated tests
    app.config.from_pyfile('local_config.py')

    # Load optional test_config                     # For automated tests
    if test_config:
        app.config.update(test_config)

    # Initialize Flask extensions
    babel = Babel(app)                              # Initialize Flask-Babel
    db = SQLAlchemy(app)                            # Initialize Flask-SQLAlchemy
    mail = Mail(app)                                # Initialize Flask-Mail

    @babel.localeselector
    def get_locale():
        translations = [str(translation) for translation in babel.list_translations()]
        return request.accept_languages.best_match(translations)

    # Define User model. Make sure to add flask.ext.user UserMixin!!
    class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        active = db.Column(db.Boolean(), nullable=False, default=False)
        username = db.Column(db.String(50), nullable=False, unique=True)
        password = db.Column(db.String(255), nullable=False, default='')
        email = db.Column(db.String(255), nullable=False, unique=True)
        confirmed_at = db.Column(db.DateTime())
        reset_password_token = db.Column(db.String(100), nullable=False, default='')
        annotator_token = db.Column(db.String(100), nullable=True)

    # Create all database tables
    db.create_all()

    # Setup Flask-User
    db_adapter = SQLAlchemyAdapter(db,  User)       # Select database adapter
    user_manager = UserManager(db_adapter, app)     # Init Flask-User and bind to app

    # Display Login page or Profile page
    @app.route('/')
    def home_page():
        if current_user.is_authenticated():
            return redirect(url_for('profile_page'))
        else:
            return redirect(url_for('user.login'))

    # The '/profile' page requires a logged-in user
    @app.route('/profile')
    @login_required
    def profile_page():
        return render_template_string("""
            {% extends "base.html" %}
            {% block content %}
                <h2>{%trans%}Profile Page{%endtrans%}</h2>
                <p> {%trans%}Hello{%endtrans%}
                    {{ current_user.username or current_user.email }},</p>
                <p> <a href="{{ url_for('user.change_username') }}">
                    {%trans%}Change username{%endtrans%}</a></p>
                <p> <a href="{{ url_for('user.change_password') }}">
                    {%trans%}Change password{%endtrans%}</a></p>
                <p> <a href="{{ url_for('user.logout') }}?next={{ url_for('user.login') }}">
                    {%trans%}Sign out{%endtrans%}</a></p>
            {% endblock %}
            """)

    return app

    def generate_token(user_id):
        return jwt.encode({
          'consumerKey': CONSUMER_KEY,
          'userId': user_id,
          'issuedAt': _now().isoformat() + 'Z',
          'ttl': CONSUMER_TTL
        }, CONSUMER_SECRET)

    def _now():
        return datetime.datetime.utcnow().replace(microsecond=0)

# Start development web server
if __name__=='__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
