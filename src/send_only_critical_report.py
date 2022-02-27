import datetime
import os

import dotenv
import sqlalchemy.orm
import telebot
from hurry.filesize import size

import database
import models

dotenv.load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = int(os.getenv('TELEGRAM_ADMIN_CHAT'))
TELEGRAM_CRITICAL_SENT_INTERVAL = int(os.getenv('TELEGRAM_CRITICAL_SENT_INTERVAL'))
CPU_CRITICAL_BOUNDARY = float(os.getenv('CPU_CRITICAL_BOUNDARY'))
RAM_CRITICAL_BOUNDARY = float(os.getenv('RAM_CRITICAL_BOUNDARY'))

bot = telebot.TeleBot(token=TELEGRAM_BOT_TOKEN)
sent_interval = datetime.datetime.now() - datetime.timedelta(minutes=TELEGRAM_CRITICAL_SENT_INTERVAL)

# Create a database connection
session: sqlalchemy.orm.Session = database.Session()

# Check CPU
cpu_info: models.CpuInfo = session.query(models.CpuInfo) \
    .order_by(sqlalchemy.desc(models.CpuInfo.timestamp)) \
    .first()

# TODO: move to a function for memory and cpu.
if cpu_info is not None and cpu_info.percent > CPU_CRITICAL_BOUNDARY:
    sent_message_info: models.SentMessages = session.query(models.SentMessages) \
        .filter(models.SentMessages.type == 'cpu_info') \
        .order_by(sqlalchemy.desc(models.SentMessages.timestamp)) \
        .first()

    if sent_message_info is None or sent_message_info.timestamp < sent_interval:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text='Critical CPU usage!\n' +
                                                        f'CPU percent usage: {cpu_info.percent}\n' +
                                                        f'CPU times user: {cpu_info.user}\n' +
                                                        f'CPU times nice: {cpu_info.nice}\n' +
                                                        f'CPU times system: {cpu_info.system}\n' +
                                                        f'CPU times idle: {cpu_info.idle}\n')

        session.add(models.SentMessages(type='cpu_info', timestamp=datetime.datetime.now()))
        session.commit()

# Check RAM
ram_info: models.RamInfo = session.query(models.RamInfo) \
    .order_by(sqlalchemy.desc(models.RamInfo.timestamp)) \
    .first()

# TODO: move to a function for memory and cpu.
if ram_info is not None and ram_info.percent > RAM_CRITICAL_BOUNDARY:
    sent_message_info: models.SentMessages = session.query(models.SentMessages) \
        .filter(models.SentMessages.type == 'ram_info') \
        .order_by(sqlalchemy.desc(models.SentMessages.timestamp)) \
        .first()

    if sent_message_info is None or sent_message_info.timestamp < sent_interval:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text='Critical RAM usage!\n' +
                                                        f'RAM percent usage: {ram_info.percent}\n' +
                                                        f'RAM total: {size(ram_info.total)}\n' +
                                                        f'RAM available: {size(ram_info.available)}\n' +
                                                        f'RAM used: {size(ram_info.used)}\n')

        session.add(models.SentMessages(type='ram_info', timestamp=datetime.datetime.now()))
        session.commit()
