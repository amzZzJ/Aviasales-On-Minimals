import os

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Text, func
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


DATABASE_URL = f"sqlite:///flights.db"


class City(Base):
    __tablename__ = 't_city'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

class Plane(Base):
    __tablename__ = 't_plane'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

class Company(Base):
    __tablename__ = 't_company'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

class Arrival(Base):
    __tablename__ = 't_arrival'

    id = Column(Integer, primary_key=True)
    city_from = Column(Integer, ForeignKey('t_city.id'), nullable=False)
    city_to = Column(Integer, ForeignKey('t_city.id'), nullable=False)
    cost = Column(Integer, nullable=False)
    plane = Column(Integer, ForeignKey('t_plane.id'), nullable=False)
    company = Column(Integer, ForeignKey('t_company.id'), nullable=False)

    from_city = relationship("City", foreign_keys=[city_from])
    to_city = relationship("City", foreign_keys=[city_to])
    plane_model = relationship("Plane", foreign_keys=[plane])
    company_model = relationship("Company", foreign_keys=[company])

class RequestCache(Base):
    __tablename__ = 't_request_cache'

    id = Column(Integer, primary_key=True)
    city_from = Column(String, nullable=False)
    city_to = Column(String, nullable=False)
    date_from = Column(String, nullable=False)
    date_to = Column(String, nullable=False)
    response = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=func.now())

flight_engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=flight_engine)
Base.metadata.create_all(flight_engine)
