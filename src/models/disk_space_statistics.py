from sqlalchemy import Column, Float, DateTime, BigInteger, String

from src.database import Base


class DiskSpaceStatistics(Base):
    __tablename__ = 'disk_space_statistics'

    mount_point = Column(String(128), name='mount_point', primary_key=True)
    timestamp = Column(DateTime, name='timestamp', primary_key=True)
    percent = Column(Float, name='percent')
    total = Column(BigInteger, name='total')
    used = Column(BigInteger, name='used')
    available = Column(BigInteger, name='available')
    device = Column(String(length=128), name='device')
