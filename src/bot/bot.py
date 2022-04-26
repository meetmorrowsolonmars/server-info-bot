from typing import List

import telebot
from sqlalchemy import desc
from sqlalchemy import orm
from telebot.types import Message

from src import config
from src.database import Session
from src.models.system_load_statistics import SystemLoadStatistics, SystemLoadType

bot = telebot.TeleBot(config.BOT_TOKEN)


@bot.message_handler(commands=['statistics'])
def get_server_statistics(message: Message):
    with Session() as session:
        session: orm.Session
        statistics: List[SystemLoadStatistics] = session \
            .query(SystemLoadStatistics) \
            .where(SystemLoadStatistics.type == SystemLoadType.CPU) \
            .order_by(desc(SystemLoadStatistics.timestamp)) \
            .limit(20) \
            .all()

    text = '\n'.join([f'{s.timestamp} {s.type} {s.percent}' for s in statistics])
    bot.send_message(message.chat.id, text)


bot.infinity_polling()
