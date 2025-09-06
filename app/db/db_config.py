import os

ENV = os.getenv("ENV", "local")  # default to local

if ENV == "local":
    DB_HOST = os.getenv("DB_HOST")  # docker-compose service name
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
else:  # Azure
    DB_HOST = os.getenv("AZURE_DB_HOST")
    DB_PORT = os.getenv("AZURE_DB_PORT", 5432)
    DB_NAME = os.getenv("AZURE_DB_NAME")
    DB_USER = os.getenv("AZURE_DB_USER")
    DB_PASSWORD = os.getenv("AZURE_DB_PASSWORD")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
