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
    full_name = Required(str)
    age = Required(int)
    #birthday = Required(date)
    birthplace = Required(str)
    team = Required('Team')
#    unique_number = Required(int)
    bike = Required('Bike')
    competitions = Set('Competition')
#    cars = Set('Car')

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
    full_name = Required(str)
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
    #birthday = Required(date)
    competitions = Set('Competition')


db.bind('sqlite', 'sqlite3.db', create_db=True)

sql_debug(True)
db.generate_mapping(create_tables=True)

@db_session
def queries():
    t1 = Team(name='team1')
    t2 = Team(name='team2')
    t3 = Team(name='team3')

    c1 = Coach(full_name='coach_1', age=60, birthplace='Vin', team=t1)
    c2 = Coach(full_name='coach_2', age=70, birthplace='Vin', team=t2)
    c3 = Coach(full_name='coach_3', age=80, birthplace='Vin', team=t3)

    b1 = Bike(kind_of_bike='bmx', made_by='Flip', material='chromo', weight=12, color='red', country='China', price=4000)
    b2 = Bike(kind_of_bike='bmx', made_by='Flip', material='chromo', weight=14, color='red', country='China', price=3000)
    b3 = Bike(kind_of_bike='bmx', made_by='Flip', material='hiten', weight=13, color='red', country='China', price=6000)
    b4 = Bike(kind_of_bike='bmx', made_by='Flip', material='chromo', weight=11, color='red', country='China', price=3000)
    b5 = Bike(kind_of_bike='bmx', made_by='Flip', material='chromo', weight=14, color='red', country='China', price=2000)



    o1 = Organizator(name="Andrew")
    o2 = Organizator(name="Petro")
    o3 = Organizator(name="Sasha")
    o4 = Organizator(name="Slava")

    comp1 = Competition(name="hillfest", country="ua", city="vn", organizator=o4)
    comp2 = Competition(name="bmxfest", country="ru", city="msk", organizator=o1)
    comp3 = Competition(name="mtbfest", country="ua", city="kiev", organizator=o2)

    p1= Participant(full_name='name1', age=19, birthplace='Vin', team=t1, bike=b1, competitions=[comp1, comp3])
    p2= Participant(full_name='name2', age=19, birthplace='Vin', team=t1, bike=b2, competitions=[comp1, comp2])
    p3= Participant(full_name='name3', age=21, birthplace='Kyiv', team=t2, bike=b3, competitions=[comp3])
    p4= Participant(full_name='name4', age=18, birthplace='Vin', team=t2, bike=b4, competitions=[comp1, comp2, comp3])
    p5= Participant(full_name='name5', age=37, birthplace='Vin', team=t2, bike=b5, competitions=[comp1, comp3])

    select(t for t in Team)[:].show()
    select(t for t in Coach)[:].show()
    select(t for t in Participant)[:].show()
    select(t for t in Organizator)[:].show()
    select(t for t in Competition)[:].show()
    select(t for t in Bike)[:].show()

queries()


from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/queries')
def queries():
    return render_template('queries.html')

@db_session
def query(id, p1, p2):
    if id == 1:
        res = select(p for p in Participant if p.age < int(p1)
                    for competition in p.competitions if competition.name == p2)[:]
        for r in res:
            r.team.name
        return res
    if id == 2:
        res = select(t for t in Team if t.name.startswith(p1)
                    for t in Team if count(t.participants) == int(p2))[:]
    if id == 3:
        return select(p for p in Participant if p.age > 0)
    if id == 4:
        return select(p for p in Participant if p.age > 0)
    if id == 5:
        return select(p for p in Participant if p.age > 0)
    if id == 6:
        return select(p for p in Participant if p.age > 0)
    if id == 7:
        return select(p for p in Participant if p.age > 0)
    if id == 8:
        return select(p for p in Participant if p.age > 0)

# /queries/5?p1=huy&p2=lok
@app.route('/queries/<query_id>')
def single_query(query_id):
    if request.args.get('p1', '') and request.args.get('p2', ''):
        p1 = request.args.get('p1', '')
        p2 = request.args.get('p2', '')
        query_result = query(int(query_id), p1, p2)
        return render_template('query_result.html', res=query_result)
    else:
        return render_template('single_query.html')



@app.route('/edit')
def all_tables():
    return render_template('all_tables.html')

@app.route('/edit/<table_name>/')
@db_session
def show_table(table_name):
    d = {
        'participant': Participant,
        'team': Team
    }
    table = d[table_name]
    res = table.select(lambda huy: True)
    return render_template('show_table.html', res=res)

@app.route('/edit/<table_name>/<int:id_raw>')
def edit_record():
    return render_template('edit_record.html')

@app.route('/edit/<table_name>/add')
def add_to_table():
    return render_template('add_to_table.html')

@app.route('/edit/<table_name>/delete')
def delete_from_table():
    return render_template('delete_from_table.html')



#url_for('static', filename='style.css')

#app.config.update(
#    DEBUG=True,
#    SECRET_KEY='...',
#    SERVER_NAME='localhost:5000'
#)
