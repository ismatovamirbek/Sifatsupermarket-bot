from environs import Env

# .env faylni o'qish
env = Env()
env.read_env()

# Token va URL
BOT_TOKEN = env.str("BOT_TOKEN")  # Telegram bot token
API_URL = env.str("API_URL")      # Backend API manzili
IP = env.str("ip")                # Hosting IP manzili

# Adminlar ro'yxati (int tipda)
ADMINS = list(map(int, env.list("ADMINS")))

GROUP_ID = -1002600360407        # Guruh ID