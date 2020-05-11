import os

class Config:
  SECRET_KEY = '06238a042bdf7a3f4bfccf1f'
  SQLALCHEMY_DATABASE_URI = 'sqlite:///champions.db'
  MAIL_SERVER = 'smtp.googlemail.com'
  MAIL_PORT = 587
  MAIL_USE_TLS = True
  MAIL_USE_SSL = False
  MAIL_USERNAME = os.environ.get('EMAIL_USER')
  MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
