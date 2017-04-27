# coding: utf-8
from flask import Flask, request, render_template
from pony.orm import *

from models import *
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
                    for c in p.competitions if c.name == p2)[:]
        for r in res:
            r.team.name
        return render_template('queryres/1.html', res=res)
    if id == 2:
        res = select(t for t in Team if t.name.startswith(p1)
                    for t in Team if count(t.participants) == int(p2))[:]
        return render_template('queryres/2.html', res=res)
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
@app.route('/queries/1')
def single_query():
    if request.args.get('p1', '') and request.args.get('p2', ''):
        p1 = request.args.get('p1', '')
        p2 = request.args.get('p2', '')
        return query(1, p1, p2)
    else:
        return render_template('queryform/1.html')



@app.route('/edit')
def all_tables():
    return render_template('all_tables.html')

@app.route('/edit/<table_name>/')
@db_session
def show_table(table_name):
    d = {
        'participant': [Participant, 'participant.html'],
        'team': [Team, 'team.html'],
        'bike': [Bike, 'bike.html'],
        'coach': [Coach, 'coach.html'],
        'competition': [Competition, 'competition.html'],
        'organizator': [Organizator, 'organizator.html']
    }
    table = d[table_name][0]
    res = table.select(lambda huy: True)
    return render_template('tableview/' + d[table_name][1] , res=res)



@db_session
@app.route('/edit/participant/add/', methods=['GET', 'POST'])
def add_participant():
    if request.method == 'POST':
        p1 = Participant(name=request.form['name'], age=request.form['age'], birthday=request.form['username'], birthplace=request.form['username'], team=Team[int(request.form['username'])], bike=Bike[int(request.form['bike'])])

    else:
        teams = Team.select(lambda c: True)
        bikes = Bike.select(lambda c: True)
        render_template('add_form/participant.html', bikes=bikes, teams=teams)


@app.route('/edit/<table_name>/delete')
def delete_from_table():
    return render_template('delete_from_table.html')
#url_for('static', filename='style.css')

#app.config.update(
#    DEBUG=True,
#    SECRET_KEY='...',
#    SERVER_NAME='localhost:5000'
#)
@db_session
def queries():
    t1 = Team(name='team1')
    t2 = Team(name='team2')
    t3 = Team(name='team3')

    c1 = Coach(name='coach_1', age=60, birthplace='Vin', team=t1)
    c2 = Coach(name='coach_2', age=70, birthplace='Vin', team=t2)
    c3 = Coach(name='coach_3', age=80, birthplace='Vin', team=t3)

    b1 = Bike(kind_of_bike='bmx', made_by='Flip', material='chromo', weight=12, color='red', country='China', price=4000)
    b2 = Bike(kind_of_bike='bmx', made_by='Flip', material='chromo', weight=14, color='red', country='China', price=3000)
    b3 = Bike(kind_of_bike='bmx', made_by='Flip', material='hiten', weight=13, color='red', country='China', price=6000)
    b4 = Bike(kind_of_bike='bmx', made_by='Flip', material='chromo', weight=11, color='red', country='China', price=3000)
    b5 = Bike(kind_of_bike='bmx', made_by='Flip', material='chromo', weight=14, color='red', country='China', price=2000)



    o1 = Organizator(name="Andrew", birthday=date.today())
    o2 = Organizator(name="Petro", birthday=date.today())
    o3 = Organizator(name="Sasha", birthday=date.today())
    o4 = Organizator(name="Slava", birthday=date.today())

    comp1 = Competition(name="hillfest", country="ua", city="vn", organizator=o4)
    comp2 = Competition(name="bmxfest", country="ru", city="msk", organizator=o1)
    comp3 = Competition(name="mtbfest", country="ua", city="kiev", organizator=o2)

    p1= Participant(name='name1', age=19, birthday=date.today(), birthplace='Vin', team=t1, bike=b1, competitions=[comp1, comp3])
    p2= Participant(name='name2', age=19, birthday=date.today(), birthplace='Vin', team=t1, bike=b2, competitions=[comp1, comp2])
    p3= Participant(name='name3', age=21, birthday=date.today(), birthplace='Kyiv', team=t2, bike=b3, competitions=[comp3])
    p4= Participant(name='name4', age=18, birthday=date.today(), birthplace='Vin', team=t2, bike=b4, competitions=[comp1, comp2, comp3])
    p5= Participant(name='name5', age=37, birthday=date.today(), birthplace='Vin', team=t2, bike=b5, competitions=[comp1, comp3])

    select(t for t in Team)[:].show()
    select(t for t in Coach)[:].show()
    select(t for t in Participant)[:].show()
    select(t for t in Organizator)[:].show()
    select(t for t in Competition)[:].show()
    select(t for t in Bike)[:].show()

queries()
