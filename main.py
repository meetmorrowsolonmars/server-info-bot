import os

import dotenv
import psutil
import telebot
from hurry.filesize import size

dotenv.load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = int(os.getenv('TELEGRAM_ADMIN_CHAT'))

bot = telebot.TeleBot(token=TELEGRAM_BOT_TOKEN)

disk_usage_format_string = 'Disk device {device} mountpoint {mountpoint}\n' + \
                           'Total: {total}\n' + \
                           'Used: {used}\n' + \
                           'Free: {free}\n' + \
                           'Percent usage: {percent}%'


def get_disk_usage_info(disk_partition) -> str:
    d = psutil.disk_usage(disk_partition.mountpoint)
    return disk_usage_format_string.format(
        device=disk_partition.device,
        mountpoint=disk_partition.mountpoint,
        total=size(d.total),
        used=size(d.used),
        free=size(d.free),
        percent=d.percent)


disk_usage = '\n\n'.join(
    map(get_disk_usage_info, [p for p in psutil.disk_partitions() if
                              'docker' not in p.mountpoint and 'snap' not in p.mountpoint]))

cpu_percent = psutil.cpu_percent(interval=1)
cpu_times_percent = psutil.cpu_times_percent(interval=1)
virtual_memory = psutil.virtual_memory()

server_info_text = f'Server status:\n' + \
                   f'CPU percent usage: {cpu_percent}%\n' + \
                   f'CPU times user: {cpu_times_percent.user}%\n' + \
                   f'CPU times nice: {cpu_times_percent.nice}%\n' + \
                   f'CPU times system: {cpu_times_percent.system}%\n' + \
                   f'CPU times idle: {cpu_times_percent.idle}%\n\n' + \
                   f'RAM percent usage: {virtual_memory.percent}%\n' + \
                   f'RAM total: {size(virtual_memory.total)}\n' + \
                   f'RAM available: {size(virtual_memory.available)}\n' + \
                   f'RAM used: {size(virtual_memory.used)}\n\n' + \
                   f'Disk usage:\n' + \
                   f'{disk_usage}\n'

bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=server_info_text)
