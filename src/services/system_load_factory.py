import datetime

import psutil

from src.models.system_load_statistics import SystemLoadStatistics, SystemLoadType


class SystemLoadFactory:

    @staticmethod
    def current_cpu_load_statistics() -> SystemLoadStatistics:
        return SystemLoadStatistics(
            type=SystemLoadType.CPU,
            timestamp=datetime.datetime.now(),
            percent=psutil.cpu_percent(interval=1),
        )

    @staticmethod
    def current_ram_load_statistics() -> SystemLoadStatistics:
        virtual_memory = psutil.virtual_memory()
        return SystemLoadStatistics(
            type=SystemLoadType.RAM,
            timestamp=datetime.datetime.now(),
            percent=virtual_memory.percent,
        )
