from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot toekn
ADMINS = env.list("ADMINS")  # adminlar ro'yxati
GROUP_CHAT_ID = env.str("GROUP_CHAT_ID")
# IP = env.str("ip")  # Xosting ip manzili

# DB_USER = env.str("DB_USER")
# DB_PASS = env.str("DB_PASS")
# DB_NAME = env.str("DB_NAME")
# DB_HOST = env.str("DB_HOST")
DEVELOPMENT_MODE = env.str("DEVELOPMENT_MODE", "False") == "True"
# DATABASE_URL = env.str("DATABASE_URL")
if DEVELOPMENT_MODE:
    DB_USER = env.str("DB_USER")
    DB_PASS = env.str("DB_PASS")
    DB_NAME = env.str("DB_NAME")
    DB_HOST = env.str("DB_HOST")
else:
    DATABASE_URL = env.str("DATABASE_URL")
