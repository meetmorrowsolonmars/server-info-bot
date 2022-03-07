import datetime
import os
import typing

import dotenv
import sqlalchemy.orm
import telebot
from hurry.filesize import size

import database
import models
import plot


def is_need_to_send_message(db_session: sqlalchemy.orm.Session, message_type: str, interval: datetime.datetime) -> bool:
    sent_message_info: models.SentMessages = db_session.query(models.SentMessages) \
        .filter(models.SentMessages.type == message_type) \
        .order_by(sqlalchemy.desc(models.SentMessages.timestamp)) \
        .first()
    return sent_message_info is None or sent_message_info.timestamp < interval


def make_plot(title: str, data: list, limit: float) -> plot.Plot:
    usage_line = plot.Line(
        [info.timestamp for info in data],
        [info.percent for info in data],
        'blue',
        '-',
        'Usage'
    )
    limit_line = plot.Line(
        [info.timestamp for info in data],
        [limit for _ in range(len(data))],
        'red',
        '-',
        'Limit'
    )
    return plot.Plot(
        title,
        'Timestamp',
        'Percent',
        data[0].timestamp,
        data[len(data) - 1].timestamp,
        0,
        100,
        [usage_line, limit_line]
    )


dotenv.load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = int(os.getenv('TELEGRAM_ADMIN_CHAT'))
TELEGRAM_CRITICAL_SENT_INTERVAL = int(os.getenv('TELEGRAM_CRITICAL_SENT_INTERVAL'))
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL'))
CPU_CRITICAL_BOUNDARY = float(os.getenv('CPU_CRITICAL_BOUNDARY'))
RAM_CRITICAL_BOUNDARY = float(os.getenv('RAM_CRITICAL_BOUNDARY'))
DISK_CRITICAL_BOUNDARY = float(os.getenv('DISK_CRITICAL_BOUNDARY'))
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
    if is_need_to_send_message(session, 'cpu_info', sent_interval):
        cpu_infos: typing.List[models.CpuInfo] = session.query(models.CpuInfo) \
            .where(models.CpuInfo.timestamp > plot_interval) \
            .order_by(sqlalchemy.asc(models.CpuInfo.timestamp)) \
            .all()
        cpu_info = cpu_infos[len(cpu_infos) - 1]

        filename = 'cpu_info.jpeg'
        info_plot = make_plot('CPU usage', cpu_infos, CPU_CRITICAL_BOUNDARY)
        info_plot.save_to_file(filename)

        with open(filename, 'rb') as plot_image:
            bot.send_photo(
                chat_id=TELEGRAM_CHAT_ID,
                photo=plot_image,
                caption='Critical CPU usage!\n' +
                        f'Current CPU percent usage: {cpu_info.percent}\n' +
                        f'Current CPU times user: {cpu_info.user}\n' +
                        f'Current CPU times nice: {cpu_info.nice}\n' +
                        f'Current CPU times system: {cpu_info.system}\n' +
                        f'Current CPU times idle: {cpu_info.idle}\n'
            )

        session.add(models.SentMessages(type='cpu_info', timestamp=datetime.datetime.now()))
        session.commit()

# Check RAM
ram_info_stmt = sqlalchemy.select(sqlalchemy.text('avg(percent) as average_percent')) \
    .where(sqlalchemy.text('timestamp > :interval')) \
    .select_from(sqlalchemy.text('ram_info'))

ram_average_percent, = session.execute(ram_info_stmt, {'interval': check_info_interval}).fetchone()

# TODO: move to a function for memory and cpu.
if ram_average_percent is not None and ram_average_percent > RAM_CRITICAL_BOUNDARY:
    if is_need_to_send_message(session, 'ram_info', sent_interval):
        ram_infos: typing.List[models.RamInfo] = session.query(models.RamInfo) \
            .where(models.RamInfo.timestamp > plot_interval) \
            .order_by(sqlalchemy.asc(models.RamInfo.timestamp)) \
            .all()
        ram_info = ram_infos[len(ram_infos) - 1]

        filename = 'ram_info.jpeg'
        info_plot = make_plot('RAM usage', ram_infos, CPU_CRITICAL_BOUNDARY)
        info_plot.save_to_file(filename)

        with open(filename, 'rb') as plot_image:
            bot.send_photo(
                chat_id=TELEGRAM_CHAT_ID,
                photo=plot_image,
                caption='Critical RAM usage!\n' +
                        f'Current RAM percent usage: {ram_info.percent}\n' +
                        f'Current RAM total: {size(ram_info.total)}\n' +
                        f'Current RAM available: {size(ram_info.available)}\n' +
                        f'Current RAM used: {size(ram_info.used)}\n'
            )

        session.add(models.SentMessages(type='ram_info', timestamp=datetime.datetime.now()))
        session.commit()

# Check disk
disk_info_stmt = sqlalchemy.select(sqlalchemy.text('mountpoint, avg(percent) as average_percent')) \
    .where(sqlalchemy.text('timestamp > :interval')) \
    .group_by(sqlalchemy.text('mountpoint')) \
    .select_from(sqlalchemy.text('disk_info'))

average_disk_info = session.execute(disk_info_stmt, {'interval': check_info_interval}).fetchall()
disk_info_lines = []

for i in average_disk_info:
    if i[1] > DISK_CRITICAL_BOUNDARY:
        disk_infos: typing.List[models.DiskInfo] = session.query(models.DiskInfo) \
            .where(models.DiskInfo.timestamp > plot_interval, models.DiskInfo.mountpoint == i[0]) \
            .order_by(sqlalchemy.asc(models.DiskInfo.timestamp)) \
            .all()

        disk_info_lines.append(plot.Line(
            [data.timestamp for data in disk_infos],
            [data.percent for data in disk_infos],
            None,
            '-',
            i[0]
        ))

if len(disk_info_lines) > 0:
    if is_need_to_send_message(session, 'disk_info', sent_interval):
        disk_info_lines.append(
            plot.Line(
                disk_info_lines[0].x_values,
                [DISK_CRITICAL_BOUNDARY for _ in range(len(disk_info_lines[0].y_values))],
                'red',
                '-',
                'Limit'
            )
        )

        filename = 'disk_info.jpeg'
        info_plot = plot.Plot(
            'DISK usage',
            'Timestamp',
            'Percent',
            disk_info_lines[0].x_values[0],
            disk_info_lines[0].x_values[len(disk_info_lines[0].x_values) - 1],
            0,
            100,
            disk_info_lines
        )
        info_plot.save_to_file(filename)

        with open(filename, 'rb') as plot_image:
            bot.send_photo(
                chat_id=TELEGRAM_CHAT_ID,
                photo=plot_image,
                caption='Critical DISK usage!'
            )

        session.add(models.SentMessages(type='disk_info', timestamp=datetime.datetime.now()))
        session.commit()
