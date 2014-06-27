
# Configure Flask
SECRET_KEY = 'secret-key-change-me'
SQLALCHEMY_DATABASE_URI = 'sqlite:///auth.sqlite'

# Configure Flask-Mail -- Required for Confirm email and Forgot password features
MAIL_SERVER   = 'smtp.mailgun.org'
MAIL_PORT     = 465
MAIL_USE_SSL  = True                            # Some servers use MAIL_USE_TLS=True instead
MAIL_USERNAME = 'user@yourdomain.com'
MAIL_PASSWORD = 'password-change-me'
MAIL_DEFAULT_SENDER = '"Admin" <info@yourdomain.com>'

# Configure Annotator JWT (JSON Web Token)
CONSUMER_KEY = 'annotateit-key-change-me'
CONSUMER_SECRET = 'annotateit-secret-change-me'

# Only change this if you're sure you know what you're doing
CONSUMER_TTL = 86400
