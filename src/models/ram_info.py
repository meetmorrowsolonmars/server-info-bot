from sqlalchemy import Column, Float, DateTime

from src.database import Base


class RamInfo(Base):
    __tablename__ = 'ram_info'

    timestamp = Column(DateTime, name='timestamp', primary_key=True)
    percent = Column(Float, name='percent', index=True)
    total = Column(Float, name='total')
    available = Column(Float, name='available')
    used = Column(Float, name='used')
