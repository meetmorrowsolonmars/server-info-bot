from sqlalchemy import Column, DateTime, String

from src.database import Base


class SentMessages(Base):
    __tablename__ = 'sent_messages'

    type = Column(String(32), name='type', primary_key=True)
    timestamp = Column(DateTime, name='timestamp', primary_key=True)
