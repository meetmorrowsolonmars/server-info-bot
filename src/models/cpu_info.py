from sqlalchemy import Column, Float, DateTime

from src.database import Base


class CpuInfo(Base):
    __tablename__ = 'cpu_info'

    timestamp = Column(DateTime, name='timestamp', primary_key=True)
    percent = Column(Float, name='percent', index=True)
    user = Column(Float, name='user')
    nice = Column(Float, name='nice')
    system = Column(Float, name='system')
    idle = Column(Float, name='idle')
