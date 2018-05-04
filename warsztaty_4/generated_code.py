# coding: utf-8
from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Index, Integer, LargeBinary, Numeric, SmallInteger, String, Table, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Actor(Base):
    __tablename__ = 'actor'

    actor_id = Column(Numeric, primary_key=True)
    first_name = Column(String(45), nullable=False)
    last_name = Column(String(45), nullable=False, index=True)
    last_update = Column(DateTime, nullable=False)


class Addres(Base):
    __tablename__ = 'address'

    address_id = Column(Integer, primary_key=True)
    address = Column(String(50), nullable=False)
    address2 = Column(String(50), server_default=text("NULL"))
    district = Column(String(20), nullable=False)
    city_id = Column(ForeignKey('city.city_id', ondelete='NO ACTION', onupdate='CASCADE'), nullable=False, index=True)
    postal_code = Column(String(10), server_default=text("NULL"))
    phone = Column(String(20), nullable=False)
    last_update = Column(DateTime, nullable=False)

    city = relationship('City')


class Category(Base):
    __tablename__ = 'category'

    category_id = Column(SmallInteger, primary_key=True)
    name = Column(String(25), nullable=False)
    last_update = Column(DateTime, nullable=False)


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


class Customer(Base):
    __tablename__ = 'customer'

    customer_id = Column(Integer, primary_key=True)
    store_id = Column(ForeignKey('store.store_id', ondelete='NO ACTION', onupdate='CASCADE'), nullable=False, index=True)
    first_name = Column(String(45), nullable=False)
    last_name = Column(String(45), nullable=False, index=True)
    email = Column(String(50), server_default=text("NULL"))
    address_id = Column(ForeignKey('address.address_id', ondelete='NO ACTION', onupdate='CASCADE'), nullable=False, index=True)
    active = Column(String(1), nullable=False, server_default=text("'Y'"))
    create_date = Column(DateTime, nullable=False)
    last_update = Column(DateTime, nullable=False)

    address = relationship('Addres')
    store = relationship('Store')


t_customer_list = Table(
    'customer_list', metadata,
    Column('ID', Integer),
    Column('name', NullType),
    Column('address', String(50)),
    Column('zip_code', String(10)),
    Column('phone', String(20)),
    Column('city', String(50)),
    Column('country', String(50)),
    Column('notes', NullType),
    Column('SID', Integer)
)


class Film(Base):
    __tablename__ = 'film'
    __table_args__ = (
        CheckConstraint("rating in ('G','PG','PG-13','R','NC-17')"),
    )

    film_id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, server_default=text("NULL"))
    release_year = Column(String(4), server_default=text("NULL"))
    language_id = Column(ForeignKey('language.language_id'), nullable=False, index=True)
    original_language_id = Column(ForeignKey('language.language_id'), index=True, server_default=text("NULL"))
    rental_duration = Column(SmallInteger, nullable=False, server_default=text("3"))
    rental_rate = Column(Numeric(4, 2), nullable=False, server_default=text("4.99"))
    length = Column(SmallInteger, server_default=text("NULL"))
    replacement_cost = Column(Numeric(5, 2), nullable=False, server_default=text("19.99"))
    rating = Column(String(10), server_default=text("'G'"))
    special_features = Column(String(100), server_default=text("NULL"))
    last_update = Column(DateTime, nullable=False)

    language = relationship('Language', primaryjoin='Film.language_id == Language.language_id')
    original_language = relationship('Language', primaryjoin='Film.original_language_id == Language.language_id')


class FilmActor(Base):
    __tablename__ = 'film_actor'

    actor_id = Column(ForeignKey('actor.actor_id', ondelete='NO ACTION', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    film_id = Column(ForeignKey('film.film_id', ondelete='NO ACTION', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    last_update = Column(DateTime, nullable=False)

    actor = relationship('Actor')
    film = relationship('Film')


class FilmCategory(Base):
    __tablename__ = 'film_category'

    film_id = Column(ForeignKey('film.film_id', ondelete='NO ACTION', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    category_id = Column(ForeignKey('category.category_id', ondelete='NO ACTION', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    last_update = Column(DateTime, nullable=False)

    category = relationship('Category')
    film = relationship('Film')


t_film_list = Table(
    'film_list', metadata,
    Column('FID', Integer),
    Column('title', String(255)),
    Column('description', Text),
    Column('category', String(25)),
    Column('price', Numeric(4, 2)),
    Column('length', SmallInteger),
    Column('rating', String(10)),
    Column('actors', NullType)
)


class FilmText(Base):
    __tablename__ = 'film_text'

    film_id = Column(SmallInteger, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)


class Inventory(Base):
    __tablename__ = 'inventory'
    __table_args__ = (
        Index('idx_fk_film_id_store_id', 'store_id', 'film_id'),
    )

    inventory_id = Column(Integer, primary_key=True)
    film_id = Column(ForeignKey('film.film_id', ondelete='NO ACTION', onupdate='CASCADE'), nullable=False, index=True)
    store_id = Column(ForeignKey('store.store_id', ondelete='NO ACTION', onupdate='CASCADE'), nullable=False)
    last_update = Column(DateTime, nullable=False)

    film = relationship('Film')
    store = relationship('Store')


class Language(Base):
    __tablename__ = 'language'

    language_id = Column(SmallInteger, primary_key=True)
    name = Column(String(20), nullable=False)
    last_update = Column(DateTime, nullable=False)


class Payment(Base):
    __tablename__ = 'payment'

    payment_id = Column(Integer, primary_key=True)
    customer_id = Column(ForeignKey('customer.customer_id'), nullable=False, index=True)
    staff_id = Column(ForeignKey('staff.staff_id'), nullable=False, index=True)
    rental_id = Column(ForeignKey('rental.rental_id', ondelete='SET NULL', onupdate='CASCADE'), server_default=text("NULL"))
    amount = Column(Numeric(5, 2), nullable=False)
    payment_date = Column(DateTime, nullable=False)
    last_update = Column(DateTime, nullable=False)

    customer = relationship('Customer')
    rental = relationship('Rental')
    staff = relationship('Staff')


class Rental(Base):
    __tablename__ = 'rental'
    __table_args__ = (
        Index('idx_rental_uq', 'rental_date', 'inventory_id', 'customer_id', unique=True),
    )

    rental_id = Column(Integer, primary_key=True)
    rental_date = Column(DateTime, nullable=False)
    inventory_id = Column(ForeignKey('inventory.inventory_id'), nullable=False, index=True)
    customer_id = Column(ForeignKey('customer.customer_id'), nullable=False, index=True)
    return_date = Column(DateTime, server_default=text("NULL"))
    staff_id = Column(ForeignKey('staff.staff_id'), nullable=False, index=True)
    last_update = Column(DateTime, nullable=False)

    customer = relationship('Customer')
    inventory = relationship('Inventory')
    staff = relationship('Staff')


t_sales_by_film_category = Table(
    'sales_by_film_category', metadata,
    Column('category', String(25)),
    Column('total_sales', NullType)
)


t_sales_by_store = Table(
    'sales_by_store', metadata,
    Column('store_id', Integer),
    Column('store', NullType),
    Column('manager', NullType),
    Column('total_sales', NullType)
)


class Staff(Base):
    __tablename__ = 'staff'

    staff_id = Column(SmallInteger, primary_key=True)
    first_name = Column(String(45), nullable=False)
    last_name = Column(String(45), nullable=False)
    address_id = Column(ForeignKey('address.address_id', ondelete='NO ACTION', onupdate='CASCADE'), nullable=False, index=True)
    picture = Column(LargeBinary, server_default=text("NULL"))
    email = Column(String(50), server_default=text("NULL"))
    store_id = Column(ForeignKey('store.store_id', ondelete='NO ACTION', onupdate='CASCADE'), nullable=False, index=True)
    active = Column(SmallInteger, nullable=False, server_default=text("1"))
    username = Column(String(16), nullable=False)
    password = Column(String(40), server_default=text("NULL"))
    last_update = Column(DateTime, nullable=False)

    address = relationship('Addres')
    store = relationship('Store', primaryjoin='Staff.store_id == Store.store_id')


t_staff_list = Table(
    'staff_list', metadata,
    Column('ID', SmallInteger),
    Column('name', NullType),
    Column('address', String(50)),
    Column('zip_code', String(10)),
    Column('phone', String(20)),
    Column('city', String(50)),
    Column('country', String(50)),
    Column('SID', Integer)
)


class Store(Base):
    __tablename__ = 'store'

    store_id = Column(Integer, primary_key=True)
    manager_staff_id = Column(ForeignKey('staff.staff_id'), nullable=False, index=True)
    address_id = Column(ForeignKey('address.address_id'), nullable=False, index=True)
    last_update = Column(DateTime, nullable=False)

    address = relationship('Addres')
    manager_staff = relationship('Staff', primaryjoin='Store.manager_staff_id == Staff.staff_id')
