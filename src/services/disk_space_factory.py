import datetime
import typing

import psutil

from src.models.disk_space_statistics import DiskSpaceStatistics


class DiskSpaceFactory:

    @staticmethod
    def current_disk_space_statistics() -> typing.List[DiskSpaceStatistics]:
        disk_space_statistics = []
        timestamp = datetime.datetime.now()

        for partition in psutil.disk_partitions():
            # TODO: add filter to config
            if 'docker' in partition.mountpoint or 'snap' in partition.mountpoint:
                continue
            disk_space_usage = psutil.disk_usage(partition.mountpoint)
            disk_space_statistics.append(DiskSpaceStatistics(
                mount_point=partition.mountpoint,
                timestamp=timestamp,
                percent=disk_space_usage.percent,
                total=disk_space_usage.total,
                used=disk_space_usage.used,
                free=disk_space_usage.free,
                device=partition.device,
            ))
        return disk_space_statistics
