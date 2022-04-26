import os

import dotenv

dotenv.load_dotenv()

# TODO: add validation for required option
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
