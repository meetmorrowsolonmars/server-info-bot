import sqlalchemy.orm

from src.database import Session
from src.services import DiskSpaceFactory

if __name__ == '__main__':
    disk_stat = DiskSpaceFactory.current_disk_space_statistics()

    with Session.begin() as session:
        session: sqlalchemy.orm.Session
        session.add_all(disk_stat)
