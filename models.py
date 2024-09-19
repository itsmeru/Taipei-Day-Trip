from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Account(Base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, nullable=True)
    user_name = Column(String(100), nullable=True)
    content = Column(Text, nullable=True)
    image_url = Column(String(255), nullable=True)
    timestamp = Column(TIMESTAMP, nullable=True, server_default=func.now(), onupdate=func.now())

class Schedule(Base):
    __tablename__ = 'schedule'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, unique=True)
    attraction_id = Column(BigInteger, nullable=False, index=True)
    date = Column(Date, nullable=False)
    time = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    attraction_id = Column(Integer, nullable=False)
    attraction_name = Column(String(255), nullable=False)
    attraction_address = Column(String(255), nullable=False)
    attraction_image = Column(String(255), nullable=False)
    trip_date = Column(Date, nullable=False)
    trip_time = Column(String(20), nullable=False)
    contact_name = Column(String(100), nullable=False)
    contact_email = Column(String(100), nullable=False)
    contact_phone = Column(String(20), nullable=False)
    status = Column(Enum('UNPAID', 'PAID', 'FAILED'), default='UNPAID')
    order_number = Column(String(255), unique=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    paid_at = Column(TIMESTAMP)
    cancelled_at = Column(TIMESTAMP)
    completed_at = Column(TIMESTAMP)
