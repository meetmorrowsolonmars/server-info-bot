from sqlalchemy import Column, Float, DateTime, String, BigInteger

from src.database import Base


class DiskInfo(Base):
    __tablename__ = 'disk_info'

    timestamp = Column(DateTime, name='timestamp', primary_key=True)
    mountpoint = Column(String(128), name='mountpoint', primary_key=True)
    device = Column(String(128), name='device')
    percent = Column(Float, name='percent', index=True)
    total = Column(BigInteger, name='total')
    used = Column(BigInteger, name='used')
    free = Column(BigInteger, name='free')
