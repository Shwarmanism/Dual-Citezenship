class Config:
    SECRET_KEY = 'This-is-very-secret-to-the-point-dev'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False