import datetime
import os
import typing

import dotenv
import matplotlib.pyplot as plt
import sqlalchemy.orm
import telebot
from hurry.filesize import size

import database
import models

dotenv.load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = int(os.getenv('TELEGRAM_ADMIN_CHAT'))
TELEGRAM_CRITICAL_SENT_INTERVAL = int(os.getenv('TELEGRAM_CRITICAL_SENT_INTERVAL'))
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL'))
CPU_CRITICAL_BOUNDARY = float(os.getenv('CPU_CRITICAL_BOUNDARY'))
RAM_CRITICAL_BOUNDARY = float(os.getenv('RAM_CRITICAL_BOUNDARY'))
PLOT_INTERVAL = int(os.getenv('PLOT_INTERVAL'))

bot = telebot.TeleBot(token=TELEGRAM_BOT_TOKEN)
sent_interval = datetime.datetime.now() - datetime.timedelta(minutes=TELEGRAM_CRITICAL_SENT_INTERVAL)
check_info_interval = datetime.datetime.now() - datetime.timedelta(minutes=CHECK_INTERVAL)
plot_interval = datetime.datetime.now() - datetime.timedelta(minutes=PLOT_INTERVAL)

# Create a database connection
session: sqlalchemy.orm.Session = database.Session()

# Check CPU
cpu_info_stmt = sqlalchemy.select(sqlalchemy.text('avg(percent) as average_percent')) \
    .where(sqlalchemy.text('timestamp > :interval')) \
    .select_from(sqlalchemy.text('cpu_info'))

cpu_average_percent, = session.execute(cpu_info_stmt, {'interval': check_info_interval}).fetchone()

# TODO: move to a function for memory and cpu.
if cpu_average_percent is not None and cpu_average_percent > CPU_CRITICAL_BOUNDARY:
    sent_message_info: models.SentMessages = session.query(models.SentMessages) \
        .filter(models.SentMessages.type == 'cpu_info') \
        .order_by(sqlalchemy.desc(models.SentMessages.timestamp)) \
        .first()

    if sent_message_info is None or sent_message_info.timestamp < sent_interval:
        cpu_infos: typing.List[models.CpuInfo] = session.query(models.CpuInfo) \
            .where(models.CpuInfo.timestamp > plot_interval) \
            .order_by(sqlalchemy.desc(models.CpuInfo.timestamp)) \
            .all()
        cpu_infos.reverse()
        cpu_info = cpu_infos[0]

        cpu_info_axis_x = [cpu_info.timestamp for cpu_info in cpu_infos]
        cpu_info_axis_y = [cpu_info.percent for cpu_info in cpu_infos]
        cpu_limit_axis_y = [CPU_CRITICAL_BOUNDARY for _ in range(len(cpu_infos))]

        fig, ax = plt.subplots()
        cpu_info_line, = ax.plot(cpu_info_axis_x, cpu_info_axis_y, 'b-', label='CPU percent')
        cpu_limit_line, = ax.plot(cpu_info_axis_x, cpu_limit_axis_y, 'r-', label='CPU limit')
        ax.legend(handles=[cpu_info_line, cpu_limit_line])

        plt.axis([cpu_infos[0].timestamp, cpu_infos[len(cpu_infos) - 1].timestamp, 0, 100])
        plt.xlabel('Timestamp')
        plt.ylabel('Percent')

        filename = 'cpu_info.jpeg'
        fig.savefig(filename)

        with open(filename, 'rb') as plot_image:
            bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=plot_image, caption='CPU plot')
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text='Critical CPU usage!\n' +
                                                        f'Current CPU percent usage: {cpu_info.percent}\n' +
                                                        f'Current CPU times user: {cpu_info.user}\n' +
                                                        f'Current CPU times nice: {cpu_info.nice}\n' +
                                                        f'Current CPU times system: {cpu_info.system}\n' +
                                                        f'Current CPU times idle: {cpu_info.idle}\n')

        session.add(models.SentMessages(type='cpu_info', timestamp=datetime.datetime.now()))
        session.commit()

# Check RAM
ram_info_stmt = sqlalchemy.select(sqlalchemy.text('avg(percent) as average_percent')) \
    .where(sqlalchemy.text('timestamp > :interval')) \
    .select_from(sqlalchemy.text('ram_info'))

ram_average_percent, = session.execute(ram_info_stmt, {'interval': check_info_interval}).fetchone()

# TODO: move to a function for memory and cpu.
if ram_average_percent is not None and ram_average_percent > RAM_CRITICAL_BOUNDARY:
    sent_message_info: models.SentMessages = session.query(models.SentMessages) \
        .filter(models.SentMessages.type == 'ram_info') \
        .order_by(sqlalchemy.desc(models.SentMessages.timestamp)) \
        .first()

    if sent_message_info is None or sent_message_info.timestamp < sent_interval:
        ram_infos: typing.List[models.RamInfo] = session.query(models.RamInfo) \
            .where(models.RamInfo.timestamp > plot_interval) \
            .order_by(sqlalchemy.desc(models.RamInfo.timestamp)) \
            .all()
        ram_infos.reverse()
        ram_info = ram_infos[0]

        ram_info_axis_x = [ram_info.timestamp for ram_info in ram_infos]
        ram_info_axis_y = [ram_info.percent for ram_info in ram_infos]
        ram_limit_axis_y = [RAM_CRITICAL_BOUNDARY for _ in range(len(ram_infos))]

        fig, ax = plt.subplots()
        ram_info_line, = ax.plot(ram_info_axis_x, ram_info_axis_y, 'b-', label='RAM percent')
        ram_limit_line, = ax.plot(ram_info_axis_x, ram_limit_axis_y, 'r-', label='RAM limit')
        ax.legend(handles=[ram_info_line, ram_limit_line])

        plt.axis([ram_infos[0].timestamp, ram_infos[len(ram_infos) - 1].timestamp, 0, 100])
        plt.xlabel('Timestamp')
        plt.ylabel('Percent')

        filename = 'ram_info.jpeg'
        fig.savefig(filename)

        with open(filename, 'rb') as plot_image:
            bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=plot_image, caption='RAM plot')
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text='Critical RAM usage!\n' +
                                                        f'Current RAM percent usage: {ram_info.percent}\n' +
                                                        f'Current RAM total: {size(ram_info.total)}\n' +
                                                        f'Current RAM available: {size(ram_info.available)}\n' +
                                                        f'Current RAM used: {size(ram_info.used)}\n')

        session.add(models.SentMessages(type='ram_info', timestamp=datetime.datetime.now()))
        session.commit()
