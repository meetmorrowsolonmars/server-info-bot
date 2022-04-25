import sqlalchemy.orm
import os

is_debug = bool(os.getenv('DEBUG'))

engine = sqlalchemy.create_engine('sqlite:///server_info.db', echo=is_debug)

Session = sqlalchemy.orm.sessionmaker(bind=engine)

Base = sqlalchemy.orm.declarative_base()
