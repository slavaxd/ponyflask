# coding: utf-8
from datetime import date

from flask import Flask, request, render_template, redirect, url_for
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
#        return res
    
    if id == 2:
        res = select(t for t in Team if t.name.startswith(p1) and count(t.participants) == int(p2))
#                    for team in Team if )[:]
#        return res
    
    if id == 3:
        res = select(c for c in Competition if c.name == p1 and count(c.participants) <= int(p2))[:]
#        return res
    
    if id == 4:
        res = select(o for o in Organizator if o.name == p1
                    for c in o.competitions if c.country == p2)[:]
#        return res
    
    if id == 5:
        res =  select(b for b in Bike if b.kind_of_bike == p1 and b.weight > int(p2))
#        return res
    
    if id == 6:
        res = select(c for c in Coach if c.team.name == p1 and c.age >= int(p2))
#        return res
    
    if id == 7:
        res = select(t for t in Team if t.coach.name == p1 and count(t.participants) >= int(p2))
#        return res
    
    if id == 8:
        res =  select(b for b in Bike if b.price == int(p1) and b.material == p2)
#        return res
    return render_template('queryres/' + str(id)     + '.html', res=res)
    
# /queries/5?p1=huy&p2=lok
@db_session
@app.route('/queries/<query_id>')
def single_query(query_id):
    if request.args.get('p1', '') and request.args.get('p2', ''):
        p1 = request.args.get('p1', '')
        p2 = request.args.get('p2', '')
#        res = query(int(query_id), p1, p2)
        return query(int(query_id), p1, p2) #render_template('queryres/' + query_id + '.html', res=res)
    else:
        return render_template('queryform/' + str(query_id) + '.html')



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

@app.route('/edit/participant/add/', methods=['GET', 'POST'])
@db_session
def add_participant():
    if request.args.get('name', ''): #request.method == 'POST':
        birthday = request.args.get('birthday').strip('-')
        birthday = map(lambda x: int(x), birthday)
        p1 = Participant(name=request.args.get('name'), age=request.args.get('age'), birthday=date(*birthday), birthplace=request.args.get('username'), team=Team[int(request.args.get('username'))], bike=Bike[int(request.args.get('bike'))])
        select(t for t in Participant)[:].show()
        return redirect('/')
    else:
        teams = Team.select(lambda c: True)
        bikes = Bike.select(lambda c: True)
#        for bike in bikes:
#            bike.name
#            team.id
#        for team in teams:
#            team.name
#            team.id
        return render_template('add_form/participant.html', bikes=bikes, teams=teams)

@app.route('/edit/<table_name>/delete/<record_id>/', methods=['GET', 'POST'])
@db_session
def delete_record(table_name, record_id):
    d = {
        'participant': Participant,
        'team': Team,
        'bike': Bike,
        'coach': Coach,
        'competition': Competition,
        'organizator': Organizator,
    }
    table = d[table_name]
    res = table.select(lambda t: t.id == int(record_id))
    
    if request.args.get('del') == '1':
        with db_session:
            res.delete()
            flush()            
        return redirect(url_for('index')) #render_template('tableview/' + d[table_name] , res=res)
    else:
        return render_template('delete_form/' + table_name + '.html', res=res)




#
#@app.route('/edit/<table_name>/delete')
#def delete_from_table():
#    return render_template('delete_from_table.html')
#url_for('static', filename='style.css')

#app.config.update(
#    DEBUG=True,
#    SECRET_KEY='...',
#    SERVER_NAME='localhost:5000'
#)
@db_session
def queries():
    t1 = Team(name='avengers', participant='John Smith', coach='c1')
    t2 = Team(name='marvel', participants='David Kapper', coach='c2')
    t3 = Team(name='universe', participants='Joe Smith ', coach='c3')
    t4 = Team(name='dc', participants='Bob Smith', coach='c4')
    t5 = Team(name='strangers', participants='Mike Smith ', coach='c5')
    t6 = Team(name='barsa', participants='Juan Carlos', coach='c6')
    t7 = Team(name='digers', participants='Jane Smith', coach='c7')
    t8 = Team(name='efiops', participants='Mike Jones', coach='c8')
    t9 = Team(name='families', participants='David Smith', coach='c9')
    t10 = Team(name='rivers', participants='Sarah Smith', coach='c10')
    t11 = Team(name='tigers', participants='James Smith', coach='c11')
    t12 = Team(name='bears', participants='Waylon Dalton', coach='c12')
    t13 = Team(name='cats', participants='Marcus Cruz', coach='c13')
    t14 = Team(name='lions', participants='Eddie Randolph', coach='c14')
    t15 = Team(name='wolves', participants='Hadassah Hartman', coach='c15')

    c1 = Coach(name='Waylon Dalton', age=51, birthday = date(1969, 3, 31), birthplace='Iceland', team=t1)
    c2 = Coach(name='Justine Henderson', age=37, birthday = date(1973, 6, 21), birthplace='Andorra', team=t2)
    c3 = Coach(name='Hadassah Hartman', age=51, birthday = date(1959, 3, 11), birthplace='Romania', team=t3)
    c4 = Coach(name='Joanna Shaffer', age=41, birthday = date(1969, 5, 13), birthplace='Romania', team=t4)
    c5 = Coach(name='Jonathon Sheppard', age=36, birthday = date(1974, 2, 26), birthplace='Andorra', team=t5)
    c6 = Coach(name='Rayne Heath', age=25, birthday = date(1975, 5, 21), birthplace='Vin', team=t6)
    c7 = Coach(name='Livia Mcgrath', age=24, birthday = date(1976, 3, 15), birthplace='Portugal', team=t7)
    c8 = Coach(name='Dakota Villanueva', age=45, birthday = date(1965, 6, 17), birthplace='Portugal', team=t8)
    c9 = Coach(name='Chance Shea', age=43, birthday = date(1957, 3, 3), birthplace='Vin', team=t9)
    c10 = Coach(name='Konnor Porter', age=23, birthday = date(1977, 9, 6), birthplace='Portugal', team=t10)
    c11 = Coach(name='Justine Henderson', age=32, birthday = date(1967, 11, 23), birthplace='England', team=t11)
    c12 = Coach(name='Sienna Barron', age=34, birthday = date(1966, 12, 13), birthplace='England', team=t12)
    c13 = Coach(name='Jayden Hess', age=35, birthday = date(1965, 11, 30), birthplace='England', team=t13)
    c14 = Coach(name='Justine Henderson', age=36, birthday = date(1964, 2, 28), birthplace='England', team=t14)
    c15 = Coach(name='Zoe Weeks', age=37, birthday = date(1963, 11, 8), birthplace='England', team=t15)

    b1 = Bike(kind_of_bike='bmx', made_by='Alcyon', material='chromo', weight=12, color='red', country='France', price=4000)
    b2 = Bike(kind_of_bike='bmx', made_by='Alcyon', material='chromo', weight=14, color='red', country='France', price=3000)
    b3 = Bike(kind_of_bike='bmx', made_by='Alcyon', material='hiten', weight=13, color='red', country='France', price=6000)
    b4 = Bike(kind_of_bike='bmx', made_by='Flip', material='chromo', weight=11, color='red', country='China', price=3000)
    b5 = Bike(kind_of_bike='bmx', made_by='Flip', material='chromo', weight=14, color='red', country='China', price=2000)
    b6 = Bike(kind_of_bike='mtb', made_by='Flip', material='chromo', weight=12, color='black', country='China', price=4000)
    b7 = Bike(kind_of_bike='mtb', made_by='Cannondale', material='chromo', weight=14, color='black', country='America', price=3000)
    b8 = Bike(kind_of_bike='mtb', made_by='Cannondale', material='hiten', weight=13, color='black', country='America', price=6000)
    b9 = Bike(kind_of_bike='mtb', made_by='Cannondale', material='chromo', weight=11, color='black', country='America', price=3000)
    b10 = Bike(kind_of_bike='mtb', made_by='Cannondale', material='chromo', weight=14, color='orange', country='America', price=2000)
    b11 = Bike(kind_of_bike='freestyle', made_by='Genesis', material='chromo', weight=12, color='orange', country='UK', price=4000)
    b12 = Bike(kind_of_bike='freestyle', made_by='Genesis', material='chromo', weight=14, color='orange', country='UK', price=3000)
    b13 = Bike(kind_of_bike='freestyle', made_by='Genesis', material='hiten', weight=13, color='orange', country='UK', price=6000)
    b14 = Bike(kind_of_bike='freestyle', made_by='Genesis', material='chromo', weight=11, color='green', country='UK', price=3000)
    b15 = Bike(kind_of_bike='freestyle', made_by='Genesis', material='chromo', weight=14, color='green', country='UK', price=2000)



    o1 = Organizator(name="Nintendo", birthday = date(1934, 4, 11), competitions='comp1')
    o2 = Organizator(name="KFC", birthday=date(1965, 1, 11), competitions='comp2')
    o3 = Organizator(name="Starbucks", birthday=date(1953, 6, 1), competitions='comp3')
    o4 = Organizator(name="Tesco", birthday=date(1973, 7, 2), competitions='comp4')
    o5 = Organizator(name="Deere", birthday=date(1946, 4, 23), competitions='comp5')
    o6 = Organizator(name="Samsung", birthday=date(1966, 6, 21), competitions='comp6')
    o7 = Organizator(name="Hyundai", birthday=date(1977, 6, 6), competitions='comp7')
    o8 = Organizator(name="Avon", birthday=date(1987, 4, 30), competitions='comp8')
    o9 = Organizator(name="Beko", birthday=date(1978, 4, 11), competitions='comp9')
    o10 = Organizator(name="Allianz", birthday=date(1990, 7, 11), competitions='comp10')
    o11 = Organizator(name="Prada", birthday=date(1979, 7, 9), competitions='comp11')
    o12 = Organizator(name="Audi", birthday=date(1988, 9, 4), competitions='comp12')
    o13 = Organizator(name="BMW", birthday=date(1987, 9, 5), competitions='comp13')
    o14 = Organizator(name="MasterCard", birthday=date(1978, 11, 3), competitions='comp14')
    o15 = Organizator(name="Sony", birthday=date(1969, 11, 8), competitions='comp15')

    comp1 = Competition(name="Hillfest", country="UK", city="London", organizator=o4)
    comp2 = Competition(name="Bmxfest", country="UK", city="London", organizator=o1)
    comp3 = Competition(name="Tourdown", country="UK", city="London", organizator=o2)
    comp4 = Competition(name="Ramptime", country="UK", city="Liverpool", organizator=o1)
    comp5 = Competition(name="Sidehop", country="UK", city="Liverpool", organizator=o2)
    comp6 = Competition(name="Bunnyrace", country="USA", city="IOWA", organizator=o4)
    comp7 = Competition(name="Hopbarfest", country="USA", city="IOWA", organizator=o1)
    comp8 = Competition(name="Faceup Tour", country="Canada", city="Alberta", organizator=o2)
    comp9 = Competition(name="Ride Side", country="Canada", city="Alberta", organizator=o1)
    comp10 = Competition(name="Fast Common", country="Canada", city="Alberta", organizator=o2)
    comp11 = Competition(name="Dirty Hill", country="Canada", city="Alberta", organizator=o4)
    comp12 = Competition(name="Fast Reload", country="Canada", city="Alberta", organizator=o1)
    comp13 = Competition(name="GitHop", country="Canada", city="Alberta", organizator=o2)
    comp14 = Competition(name="Ranhob Gast", country="USA", city="Minnesota", organizator=o1)
    comp15 = Competition(name="Guntfest", country="USA", city="Minnesota", organizator=o2)

    p1= Participant(name='Швець Олег Микитович', age=40, birthday = date(1957, 5, 31), birthplace='Ukraine', team=t1, bike=b1, competitions=[comp1, comp2, comp4, comp3])
    p2= Participant(name='Пайков Карп Иванович', age=30, birthday = date(1980, 3, 30), birthplace='Russia', team=t2, bike=b2, competitions=[comp8, comp15])
    p3= Participant(name='Жиленков Георгий Сергеевич', age=30, birthday = date(1980, 7, 30), birthplace='Russia', team=t2, bike=b3, competitions=[comp9, comp10, comp7, comp6])
    p4= Participant(name='Стасенко Андрій Віталійович', age=18, birthday = date(1989, 2, 4), birthplace='Ukraine', team=t1, bike=b4, competitions=[comp4, comp5, comp3])
    p5= Participant(name='Farmer Robert', age=37, birthday = date(1983, 7, 6), birthplace='USA', team=t3, bike=b5, competitions=[comp11, comp12, comp15, comp5])
    p6= Participant(name='Hudson Oliver', age=19, birthday = date(1993, 9, 3), birthplace='USA', team=t6, bike=b6, competitions=[comp3, comp14, comp6, comp7])
    p7= Participant(name='Collins Byron', age=19, birthday = date(1993, 2, 16), birthplace='USA', team=t3, bike=b7, competitions=[comp4, comp8])
    p8= Participant(name='Allen Benjamin', age=21, birthday = date(1989, 5, 26), birthplace='USA', team=t5, bike=b8, competitions=[comp3, comp3, comp14, comp15])
    p9= Participant(name='McCoy Brendan', age=18, birthday = date(1989, 3, 31), birthplace='USA', team=t4, bike=b9, competitions=[comp8, comp4, comp6])
    p10= Participant(name='Hopkins Gerald', age=37, birthday = date(1969, 4, 12), birthplace='UK', team=t6, bike=b10, competitions=[comp10, comp6, comp4, comp9])
    p11= Participant(name='Holt Shon', age=19, birthday = date(1991, 6, 13), birthplace='UK', team=t1, bike=b11, competitions=[comp3, comp13])
    p12= Participant(name='Joseph Dustin', age=19, birthday = date(1991, 3, 24), birthplace='UK', team=t3, bike=b12, competitions=[comp15, comp12])
    p13= Participant(name='Small Gilbert', age=21, birthday = date(1989, 11, 27), birthplace='UK', team=t5, bike=b13, competitions=[comp3])
    p14= Participant(name='Young David', age=18, birthday = date(1992, 11, 25), birthplace='Canada', team=t4, bike=b14, competitions=[comp3, comp5, comp10])
    p15= Participant(name='Fox Simon', age=37, birthday = date(1978, 12, 22), birthplace='Canada', team=t6, bike=b15, competitions=[comp8, comp10, comp1, comp11])

    select(t for t in Team)[:].show()
    select(t for t in Coach)[:].show()
    select(t for t in Participant)[:].show()
    select(t for t in Organizator)[:].show()
    select(t for t in Competition)[:].show()
    select(t for t in Bike)[:].show()

queries()
