import datetime

import dotenv
import psutil
import sqlalchemy.orm

import database
import models

dotenv.load_dotenv()

timestamp = datetime.datetime.now()

# Get information about the use of disks.
disk_info = []

for partition in psutil.disk_partitions():
    if 'docker' in partition.mountpoint or 'snap' in partition.mountpoint:
        continue
    disk_usage = psutil.disk_usage(partition.mountpoint)
    disk_info.append(models.DiskInfo(
        timestamp=timestamp,
        device=partition.device,
        mountpoint=partition.mountpoint,
        percent=disk_usage.percent,
        total=disk_usage.total,
        used=disk_usage.used,
        free=disk_usage.free,
    ))

# Get information about the use of CPU.
cpu_times_percent = psutil.cpu_times_percent(interval=1)
cpu_info = models.CpuInfo(
    timestamp=timestamp,
    percent=psutil.cpu_percent(interval=1),
    user=cpu_times_percent.user,
    nice=cpu_times_percent.nice,
    system=cpu_times_percent.system,
    idle=cpu_times_percent.idle,
)

# Get information about the use of RAM.
virtual_memory = psutil.virtual_memory()
ram_info = models.RamInfo(
    timestamp=timestamp,
    percent=virtual_memory.percent,
    total=virtual_memory.total,
    available=virtual_memory.available,
    used=virtual_memory.used,
)

# Save to database
session: sqlalchemy.orm.Session = database.Session()
session.add_all(disk_info)
session.add(cpu_info)
session.add(ram_info)
session.commit()
session.close()
