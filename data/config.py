"""
Здесь на основе данных из .env файла создаются глобальные переменные служебного назначения:
    BOT_TOKEN: Токен бота.
    ADMINS: Список ID админов бот.
    IP: IP-адрес хоста.
    DB_USER: Имя пользователя БД Postgres.
    DB_PASS: Пароль БД Postgres.
    DB_NAME: Название БД Postgres.
    DB_HOST: Хост БД Postgres.
    POSTGRES_URI: Адрес подключения к БД Postgres.
"""

from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
IP = env.str("ip")

DB_USER = env.str("DB_USER")
DB_PASS = env.str("DB_PASS")
DB_NAME = env.str("DB_NAME")
DB_HOST = env.str("DB_HOST")

POSTGRES_URI = f"postgresql://{DB_USER}:{DB_PASS}@{IP}/{DB_NAME}"
