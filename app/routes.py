import re
from app import app
from app import db
from flask import Flask, request, jsonify
from .models import db, Employee, Horse, Task, News, EmployeesNews
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import datetime
from sqlalchemy import desc, asc


@app.before_first_request
def drop_create():
    db.drop_all()
    db.create_all()
    boss = Employee(
        first_name='Małgorzata',
        last_name='Leśniak',
        born='1992-03-23',
        position='szef',
        email='lesniak@gmail.com',
        phone_number=502384567,
        password='ilovemymom',
    )
    db.session.add(boss)
    db.session.commit()
    fill_data()


jwt = JWTManager(app)

"""
ENDPOINTS:
@app.route('/employee/create', methods=['POST'])
@app.route('/employees', methods=['GET'])
@app.route('/employee/<id>', methods=['GET'])
@app.route('/employee/<id>/update', methods=['GET, POST'])
@app.route('/employee/<id>/delete', methods=['GET', 'POST'])
@app.route('/horse/create', methods=['POST'])
@app.route('/horses', methods=['GET'])
@app.route('/horse/<id>', methods=['GET'])
@app.route('/horse/<id>/update', methods=['POST'])
@app.route('/horse/<id>/delete', methods=['GET', 'POST'])
@app.route('/task/create', methods=['POST'])
@app.route('/tasks', methods=['GET'])
@app.route('/task/<id>', methods=['GET'])
@app.route('/task/<id>/update', methods=['POST'])
@app.route('/task/<id>/delete', methods=['GET', 'POST'])
@app.route('/news/create', methods=['POST'])
@app.route('/newses', methods=['GET'])
@app.route('/news/<id>', methods=['GET'])
@app.route('/news/<id>/update', methods=['POST'])
@app.route('/news/<id>/delete', methods=['GET', 'POST'])
@app.route('/rebuild_all')
"""

@app.route('/', methods=['GET'])
def routes_list():
    func_list = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            func_list.append(rule.rule)
    return jsonify({"endpoints": func_list})

#  employee
@app.route('/employee/create', methods=['POST'])
@jwt_required()
def add_employee():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    born = request.json['born']
    email = request.json['email']
    phone_number = request.json['phone_number']
    password = request.json['password']
    position = request.json['position']

    if Employee.find_by_email(email):
        return jsonify({"msg": "A user with that username already exists"}), 400

    employee = Employee(
        first_name=first_name,
        last_name=last_name,
        born=born,
        email=email,
        phone_number=phone_number,
        password=password,
        position=position,

    )
    try:
        db.session.add(employee)
        db.session.commit()
    except:
        return jsonify({"msg": "An error occurred inserting the item."}), 500
    return jsonify(employee.serialize()), 200


@app.route('/employees', methods=['GET'])
@jwt_required()
def get_employees():
    employees = Employee.query.all()
    json_employees = []
    for employee in employees:
        json_employees.append(employee.serialize())
    return jsonify(json_employees)


@app.route('/employee/<id>', methods=['GET'])
@jwt_required()
def get_employee(id):
    employee = Employee.query.get(id)
    if employee:
        return jsonify(employee.serialize()), 200
    else:
        return jsonify({"msg": f"Employee with id: {id} not found"}), 404


@app.route('/employee/<id>/update', methods=['POST'])
@jwt_required()
def update_employee(id):
    employee = Employee.query.get(id)
    if employee:
        employee.first_name = request.json['first_name']
        employee.last_name = request.json['last_name']
        employee.born = request.json['born']
        employee.email = request.json['email']
        employee.position = request.json['position']
        employee.phone_number = request.json['phone_number']
        employee.password = request.json['password']
        try:
            db.session.commit()
        except:
            return jsonify({"msg": "An error occurred updating the item."}), 500
        return jsonify({"msg": f"Employee with id: {id} updated"}), 200
    return jsonify({"msg": f"Employee with id: {id} not found"}), 404


@app.route('/employee/<id>/delete', methods=['GET', 'POST'])
@jwt_required()
def delete_employee(id):
    employee = Employee.query.get(id)
    if employee:
        try:
            db.session.delete(employee)
            db.session.commit()
        except:
            return jsonify({"msg": "An error occurred deleting the item."}), 500
        return jsonify(f"Employee with id: {id} has been deleted"), 200
    return jsonify({"msg": f"Employee with id: {id} not found"}), 404


@app.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']
    employee = Employee.find_by_email(email)
    if employee and employee.password == password:
        access_token = create_access_token(
            identity=employee.id, fresh=True, expires_delta=datetime.timedelta(seconds=86400)) # one day
        return jsonify({
            'access_token': access_token,
            'employee_id': employee.id,
            'user_position': employee.position,
            'expires_in': 86400
        }), 200
    return jsonify({"msg": "Invalid Credentials!"}), 401


#  horse
@app.route('/horse/create', methods=['POST'])
@jwt_required()
def add_horse():
    name = request.json['name']
    father = request.json['father']
    mother = request.json['mother']
    born = request.json['born']
    horse_coat = request.json['horse_coat']
    owner = request.json['owner'],
    image_name = request.json['image_name'],
    description = request.json['description']

    horse = Horse(
        name=name,
        father=father,
        mother=mother,
        born=born,
        horse_coat=horse_coat,
        owner=owner,
        image_name=image_name,
        description=description,
    )
    try:
        db.session.add(horse)
        db.session.commit()
    except:
        return jsonify({"msg": "An error occurred inserting the item."}), 500
    return jsonify(horse.serialize()), 200


@app.route('/horses', methods=['GET'])
def get_horses():
    horses = Horse.query.all()
    json_horses = []
    for horse in horses:
        json_horses.append(horse.serialize())
    return jsonify(json_horses)


@app.route('/horse/<id>', methods=['GET'])
def get_horse(id):
    horse = Horse.query.get(id)
    if horse:
        return jsonify(horse.serialize()), 200
    else:
        return jsonify({"msg": f"Horse with id: {id} not found"}), 404


@app.route('/horse/<id>/update', methods=['POST'])
@jwt_required()
def update_horse(id):
    horse = Horse.query.get(id)
    if horse:
        horse.father = request.json['father']
        horse.mother = request.json['mother']
        horse.born = request.json['born']
        horse.horse_coat = request.json['horse_coat']
        horse.owner = request.json['owner']
        horse.image_name = request.json['image_name']
        horse.description = request.json['description']
        try:
            db.session.commit()
        except:
            return jsonify({"msg": "An error occurred updating the item."}), 500
        return jsonify({"msg": f"Horse with id: {id} updated"}), 200
    return jsonify({"msg": f"Horse with id: {id} not found"}), 404


@app.route('/horse/<id>/delete', methods=['POST'])
@jwt_required()
def delete_horse(id):
    horse = Horse.query.get(id)
    if horse:
        try:
            db.session.delete(horse)
            db.session.commit()
        except:
            return jsonify({"msg": "An error occurred deleting the item."}), 500
        return jsonify({"msg": f"Horse with id: {id} has been deleted"}), 200
    return jsonify({"msg": f"Horse with id: {id} not found"}), 404


#  task
@app.route('/task/create', methods=['POST'])
@jwt_required()
def add_task():
    employee = request.json['employee']
    title = request.json['title']
    date = request.json['date']
    description = request.json['description']
    status = request.json['status']
    task = Task(
        employee=employee,
        title=title,
        date=date,
        description=description,
        status=status
    )
    try:
        db.session.add(task)
        db.session.commit()
    except:
        return jsonify({"msg": "An error occurred inserting the item."}), 500
    return jsonify(task.serialize()), 200


@app.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    sort = request.args.get('sort')
    filter = request.args.get('filter')
    if filter:
        filterValues = filter.split('-')
        if filterValues[0] == 'employee' and filterValues[1]:
            tasks = Task.query.filter(Task.employee.in_(
                [i for i in filterValues[1].split(',')])).all()

    elif sort == 'date':
        tasks = Task.query.order_by(asc(Task.date)).all()
    elif sort == '-date':
        tasks = Task.query.order_by(desc(Task.date)).all()
    else:
        tasks = Task.query.all()

    json_tasks = []
    for task in tasks:
        json_tasks.append(task.serialize())

    return jsonify(json_tasks)


@app.route('/task/<id>', methods=['GET'])
@jwt_required()
def get_task(id):
    task = Task.query.get(id)
    if task:
        return jsonify(task.serialize()), 200
    else:
        return jsonify({"msg": f"Task with id: {id} not found"}), 404


@app.route('/task/<id>/update', methods=['POST'])
@jwt_required()
def update_task(id):
    task = Task.query.get(id)
    if task:
        task.date = request.json['date']
        task.employee = request.json['employee']
        task.title = request.json['title']
        task.description = request.json['description']
        task.status = request.json['status']
        try:
            db.session.commit()
        except:
            return jsonify({"msg": "An error occurred updating the item."}), 500
        return jsonify({"msg": f"Task with id: {id} updated"}), 200
    return jsonify({"msg": f"Task with id: {id} not found"}), 404


@app.route('/task/<id>/delete', methods=['POST'])
@jwt_required()
def delete_task(id):
    task = Task.query.get(id)
    if task:
        try:
            db.session.delete(task)
            db.session.commit()
        except:
            return jsonify({"msg": "An error occurred deleting the item."}), 500
        return jsonify({"msg": f"Task with id: {id} has been deleted"}), 200
    return jsonify({"msg": f"Task with id: {id} not found"}), 404


# news
@app.route('/news/create', methods=['POST'])
@jwt_required()
def add_news():
    date = request.json['date']
    title = request.json['title']
    description = request.json['description']
    author = request.json['author']
    news = News(
        date=date,
        title=title,
        description=description,
        author=author
    )
    try:
        db.session.add(news)
        db.session.commit()
    except:
        return jsonify({"msg": "An error occurred inserting the item."}), 500
    return jsonify(news.serialize()), 200


@app.route('/newses', methods=['GET'])
def get_newses():
    newses = News.query.order_by(desc(News.date)).all()
    json_newses = []
    for news in newses:
        json_newses.append(news.serialize())

    return jsonify(json_newses)


@app.route('/news/<id>', methods=['GET'])
def get_news(id):
    news = News.query.get(id)
    if news:
        return jsonify(news.serialize()), 200
    else:
        return jsonify({"msg": f"News with id: {id} not found"}), 404


@app.route('/news/<id>/update', methods=['POST'])
@jwt_required()
def update_news(id):
    news = News.query.get(id)
    if news:
        news.date = request.json['date']
        news.title = request.json['title']
        news.description = request.json['description']
        news.author = request.json['author']
        try:
            db.session.commit()
        except:
            return jsonify({"msg": "An error occurred updating the item."}), 500
        return jsonify({"msg": f"News with id: {id} updated"}), 200
    return jsonify({"msg": f"News with id: {id} not found"}), 404


@app.route('/news/<id>/delete', methods=['GET', 'POST'])
@jwt_required()
def delete_news(id):
    new = News.query.get(id)
    if new:
        try:
            db.session.delete(new)
            db.session.commit()
        except:
            return jsonify({"msg": "An error occurred deleting the item."}), 500
        return jsonify({"msg": f"News with id: {id} has been deleted"}), 200
    return jsonify({"msg": f"News with id: {id} not found"}), 404

# employees news


@app.route('/employees_news/create', methods=['POST'])
@jwt_required()
def add_employees_news():
    date = request.json['date']
    title = request.json['title']
    description = request.json['description']
    author = request.json['author']
    employees_news = EmployeesNews(
        date=date,
        title=title,
        description=description,
        author=author
    )
    try:
        db.session.add(employees_news)
        db.session.commit()
    except:
        return jsonify({"msg": "An error occurred inserting the item."}), 500
    return jsonify(employees_news.serialize()), 200


@app.route('/employees_newses', methods=['GET'])
@jwt_required()
def get_employees_newses():
    employees_newses = EmployeesNews.query.order_by(
        desc(EmployeesNews.date)).all()
    json_newses = []
    for news in employees_newses:
        json_newses.append(news.serialize())
    return jsonify(json_newses)


@app.route('/employees_news/<id>', methods=['GET'])
@jwt_required()
def get_employees_news(id):
    employees_news = EmployeesNews.query.get(id)
    if employees_news:
        return jsonify(employees_news.serialize()), 200
    else:
        return jsonify({"msg": f"Employee news with id: {id} not found"}), 404


@app.route('/employees_news/<id>/update', methods=['POST'])
@jwt_required()
def update_employees_news(id):
    employees_news = EmployeesNews.query.get(id)
    if employees_news:
        employees_news.date = request.json['date']
        employees_news.title = request.json['title']
        employees_news.description = request.json['description']
        employees_news.author = request.json['author']
        try:
            db.session.commit()
        except:
            return jsonify({"msg": "An error occurred updating the item."}), 500
        return jsonify({"msg": f"Employee news with id: {id} updated"}), 200
    return jsonify({"msg": f"Employee news with id: {id} not found"}), 404


@app.route('/employees_news/<id>/delete', methods=['GET', 'POST'])
@jwt_required()
def delete_employees_news(id):
    employees_new = EmployeesNews.query.get(id)
    if employees_new:
        try:
            db.session.delete(employees_new)
            db.session.commit()
        except:
            return jsonify({"msg": "An error occurred deleting the item."}), 500
        return jsonify({"msg": f"Employee news with id: {id} has been deleted"}), 200
    return jsonify({"msg": f"Employee news with id: {id} not found"}), 404


#  rebuild database
def re_build():
    try:
        db.drop_all()
        db.create_all()
    except:
        return jsonify({"msg": "Dropping and creating database failed"}), 500
    return jsonify({"msg": "Database has been rebuild"}), 200


#  fill db with example data
def fill_data():
    password = 'tajne_haslo123'
    employee = Employee(
        first_name='Matuesz',
        last_name='Strojny',
        born='1992-03-23',
        position='pracownik',
        email='mateusz.wajche@gmail.com',
        phone_number=321234123,
        password=password,
    )
    employee2 = Employee(
        first_name='Daria',
        last_name='Misiecka',
        born='2000-09-07',
        email='darson@gmail.com',
        phone_number=234123123,
        position='pracownik',
        password='dariuszka1',

    )
    boss = Employee(
        first_name='Anastazja',
        last_name='Hołda',
        born='1999-09-22',
        position='szef',
        email='anastazja@gmail.com',
        phone_number=533556879,
        password=password,

    )
    balada = Horse(
        name='Balada',
        father='NN',
        mother='NN',
        born='2010-01-01',
        horse_coat='siwa',
        owner='Daria Misiecka',
        image_name='siwa.jpg',
        description='Balada, potocznie zwana Siwą jest z nami od roku. Jest bardzo odważna, uwielbia tereny i rajdy. Prawie zawsze na czele. Czasami się zezłości i stuli uszy, ale spokojnie! To tylko na pokaz.',
    )
    gejsza = Horse(
        name='Gejsza',
        father='Statut',
        mother='Gaja',
        born='2009-04-24',
        horse_coat='gniada',
        owner='Małgorzata Leśniak',
        image_name='gejsza.jpg',
        description='Ulubienica właścicielki naszej stajni i jej prywatny koń. Gejsza po swoim tacie, rasy pełnej krwi angielskiej, odziedziczyła temperament. W obejściu typ miśka - odpala się pod siodłem. ',
    )
    galermo = Horse(
        name='Galermo',
        father='Drops',
        mother='Guma',
        born='2010-01-01',
        horse_coat='gniady',
        owner='Małgorzata Leśniak',
        image_name='galermo.jpg',
        description='Galermo to drugi, prywatny koń właścicielki. To jeszcze młodziak, więc głowę ma pełną różnych pomysłów (nie zawsze mądrych). Mówimy na niego "dziecko wojny", ponieważ ciągle sobie coś uszkadza:) Niedawno zaczął prace pod siodłem.',
    )
    bagoda = Horse(
        name='Bagoda',
        father='Devin du Maury',
        mother='Bartella',
        born='2009-05-21',
        horse_coat='ksztanowata',
        owner='Gabriela Stasiowska',
        image_name='bagoda.jpg',
        description='Bagoda, dzierżawiona przez jeźdźca z naszej stadniny - Gabrysię, jest koniem sportowym. Wspólnie z Gabi, jeżdżą na zawody sportowe w skokach przez przeszkody. Jest to koń pod jednego jeźdźca, dlatego często nikt, poza Gabi, nie może się z nią dogadać. We wcześniejszych stadninach dawała piękne źrebaki.',
    )
    mak = Horse(
        name='Mak',
        father='Pinokio',
        mother='Maja',
        born='2010-01-01',
        horse_coat='gniady',
        owner='Anastazja Hołda',
        image_name='mak.jpg',
        description='Makuś to kucyk, ikona naszej stadniny. Niesamowicie inteligentny konik, odważny i zdziorny - jak to kucyk. Jest oczyma naszego patrona Dawida. Jeżdżą na nim zarówno początkujący adepci jeździectwa, jak i doświadczone osoby. Pięknie skacze przez przeszkody - i to nie takie małe.',
    )
    perla = Horse(
        name='Perła',
        father='Lord',
        mother='Pola',
        born='2009-01-01',
        horse_coat='taranotwa',
        owner='Stadnina Dworska',
        image_name='perla.jpg',
        description='Perełka to jescze młody koń, ale już zachowuje się jak profesor. Niesamowicie spokojna, odważna. Również jeździ na zawody skokowe. Przez to, że jest tak grzeczna, każdy się z nią dogada.',
    )
    db.session.add(employee)
    db.session.add(employee2)
    db.session.add(boss)
    db.session.add(gejsza)
    db.session.add(balada)
    db.session.add(galermo)
    db.session.add(bagoda)
    db.session.add(perla)
    db.session.add(mak)
    db.session.commit()
    task = Task(
        title='Obtarcie Partycy',
        description='Pyśka jest obtarta pod popręgiem. Zasmarować Alantanem.',
        date='2021-05-05',
        employee=employee2.id,
        status='nowe'
    )
    task2 = Task(
        title='Grodzenie',
        description='Ogrodzić pastuchem na prawym padoku - Mak wychodzi.',
        employee=employee.id,
        date='2021-06-05',
        status='w realizacji'
    )
    task5 = Task(
        title='Wybranie obornika',
        description='W sobotę o 11 wybrać obornik od koni',
        employee=employee.id,
        date='2021-05-11',
        status='w realizacji'
    )
    task3 = Task(
        title='Ścielenie boksów',
        description='Pościelić boksy rano po karmieniu',
        employee=employee.id,
        date='2021-05-21',
        status='zaakceptowane'
    )
    task4 = Task(
        title='Wysłać Pani Anastazji zgody',
        description='Zgody na wzięcie udziału w półkoloniach - do niedzieli!',
        employee=employee2.id,
        date='2021-01-05',
        status="odrzucone"
    )
    task6 = Task(
        title='Wysłać Gosi rozliczenie',
        description='!',
        employee=boss.id,
        date='2021-01-05',
        status="nowe"
    )
    news1 = News(
        date='2021-03-02',
        title='Zawody!',
        description='W naszym ośrodku będą odbywać się zawody. Start zaplanowany jest na godzinę 11:00 w sobotę 13 września 2021r. Zaczniemy od parkouru o wysokości 50cm, następnie przejdziemy do 80cm. SERDECZNIE ZAPRASZAMY',
        author=boss.id,
    )
    news2 = News(
        date='2021-03-12',
        title='Witaj Kapitanie!',
        description='Mamy przyjemność powiadomić, że w naszej stajni pojawił się nowy koń - Kapitan. Już niedługo będzie uczył naszych młodych adeptów jeździectwa. Zobaczycie go już na kolejnej jeździe :)',
        author=employee2.id,
    )
    news3 = News(
        date='2021-07-02',
        title='Zawody w Zabajce.',
        description='W niedzielę 23 sierpnia wybieramy się na zawody skokowe. Reprezentować będzie nas Gabrysia Stasiowska na koniu Bagoda oraz Wiktoria Lonc na koniu Perła. Życzymy powodzenia!',
        author=boss.id,
    )
    news4 = News(
        date='2021-06-02',
        title='Ruszają półkolonie',
        description='We wakacje odbędą się półkolonie w naszej stajni. Zapisy tylko telefonicznine u Pani Anastazji. Kontakt znajdziecie na stronie głownej strony:)',
        author=boss.id,
    )
    news5 = News(
        date='2021-07-20',
        title='Nowy instruktor',
        description='Miło powitać nam nowego instruktora w naszej stajni:) To Pan Leszek! Życzymy grzecznych uczniów oraz cierpliwości do naszych koników!',
        author=employee.id,
    )
    db.session.add(task)
    db.session.add(task2)
    db.session.add(task3)
    db.session.add(task4)
    db.session.add(task5)
    db.session.add(task6)
    db.session.add(news1)
    db.session.add(news2)
    db.session.add(news3)
    db.session.add(news4)
    db.session.add(news5)
    db.session.commit()
    employeeNews = EmployeesNews(
        date='2021-01-14',
        title='Weterynarz w środę',
        description='Sebastian Maj przyjeżdża w środę do naszej stajni. Gdyby ktoś miał jakieś uwagi/prośby do niego prosze zgłaszać do mnie.',
        author='1',
    )
    employeeNews2 = EmployeesNews(
        date='2021-01-14',
        title='Bagoda wraca',
        description='Bagoda wraca z Toporzyska w sobotę. Fajnie by było, gdyby ktoś był i pomógł mi ją wyładować z przyczepy.',
        author=employee.id,
    )
    employeeNews3 = EmployeesNews(
        date='2021-01-14',
        title='Galermo - stan zapalny',
        description='Któreś użarło klatke piersiowa galusia - nie puszczamy go na prawy padok, bo będzie urażał to o barierki. Tylko na pastuch!',
        author=employee2.id
    )
    employeeNews4 = EmployeesNews(
        date='2021-01-14',
        title='Dostawa trocin',
        description='Trociny dla Perły przyjdą w piątek. Ścielić jej tylko nimi!',
        author=1
    )
    db.session.add(employeeNews)
    db.session.add(employeeNews2)
    db.session.add(employeeNews3)
    db.session.add(employeeNews4)
    db.session.commit()
    return jsonify({"msg": "Data added"}), 200
