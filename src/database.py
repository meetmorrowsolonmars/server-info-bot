import sqlalchemy.orm

engine = sqlalchemy.create_engine('sqlite:///server_info.db', echo=True)

Session = sqlalchemy.orm.sessionmaker(bind=engine)

Base = sqlalchemy.orm.declarative_base()
