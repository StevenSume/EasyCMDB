class Config:
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@hostname/dbname'
    SECRET_KEY = 'secret_key'
    TOKEN_EXPIRES_IN = 600
    USERNAME='admin'
    PASSWORD='admin'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True

    @staticmethod
    def init_app(app):
        pass