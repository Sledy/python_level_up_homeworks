from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import sqlacodegen

Base = automap_base()

engine = create_engine("sqlite:///database.db")
Base.prepare(engine, reflect=True)
print(Base.classes.actor)

print(repr(Base.classes.actor.__table__))

sqlacodegen sqlite:///database.db