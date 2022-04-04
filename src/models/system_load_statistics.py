import enum

from sqlalchemy import Column, Float, DateTime, Enum

from src.database import Base


class SystemLoadType(enum.Enum):
    CPU = 'cpu'
    RAM = 'ram'


class SystemLoadStatistics(Base):
    __tablename__ = 'system_load_statistics'

    type = Column(Enum(SystemLoadType), name='type', primary_key=True)
    timestamp = Column(DateTime, name='timestamp', primary_key=True)
    percent = Column(Float, name='percent')
