import sqlalchemy.orm

from src.database import Session
from src.services.system_load_factory import SystemLoadFactory

if __name__ == '__main__':
    cpu_stat = SystemLoadFactory.current_cpu_load_statistics()
    ram_stat = SystemLoadFactory.current_ram_load_statistics()

    with Session.begin() as session:
        session: sqlalchemy.orm.Session
        session.add_all([cpu_stat, ram_stat])
