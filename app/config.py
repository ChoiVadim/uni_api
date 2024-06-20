import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "1234")
    SQLALCHEMY_DATABASE_URI = "sqlite:///univdb-sqlite.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "12345")
    JWT_ACCESS_TOKEN_EXPIRES = 3600
    JWT_REFRESH_TOKEN_EXPIRES = 86400
