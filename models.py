# coding: utf-8
from datetime import date

from pony.orm import *

db = Database()

class Team(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    participants = Set('Participant')
    coach = Optional('Coach')

class Participant(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    age = Required(int)
    birthday = Required(date)
    birthplace = Required(str)
    team = Required('Team')
    bike = Required('Bike')
    competitions = Set('Competition')


class Bike(db.Entity):
    id = PrimaryKey(int, auto=True)
    kind_of_bike = Required(str)
    made_by = Required(str)
    material = Required(str)
    weight = Required(int)
    color = Required(str)
    country = Required(str)
    price = Required(int)
    participant = Optional('Participant')

class Coach(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    age = Required(int)
#    birthday = Required(date)
    birthplace = Required(str)
    team = Required('Team')

class Competition(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    country = Required(str)
    city = Required(str)
    organizator = Required('Organizator')
    participants = Set('Participant')


class Organizator(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    birthday = Required(date)
    competitions = Set('Competition')


db.bind('sqlite', 'sqlite3.db', create_db=True)

sql_debug(True)
db.generate_mapping(create_tables=True)




