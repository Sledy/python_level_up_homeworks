# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, SmallInteger, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class City(Base):
    __tablename__ = 'city'

    city_id = Column(Integer, primary_key=True)
    city = Column(String(50), nullable=False)
    country_id = Column(ForeignKey('country.country_id', ondelete='NO ACTION', onupdate='CASCADE'), nullable=False, index=True)
    last_update = Column(DateTime, nullable=False)

    country = relationship('Country')


class Country(Base):
    __tablename__ = 'country'

    country_id = Column(SmallInteger, primary_key=True)
    country = Column(String(50), nullable=False)
    last_update = Column(DateTime)

