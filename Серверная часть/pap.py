import json
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask import send_from_directory
import psycopg2
import datetime
import matplotlib as mpl

mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import csv

app = Flask(__name__)

conn = psycopg2.connect(database='hackathon', user='postgres', password='gennadi0', host='127.0.0.1', port=5432)
cur = conn.cursor()


@app.route("/update", methods=['POST'])
def update():
    dict = {}
    print(request.get_json())
    name = request.get_json()
    cur.execute("INSERT INTO workers (id, name, surname) VALUES (%s, %s, %s)", (name.get('id'), (name.get('name')),
                                                                                name.get('surname')))
    conn.commit()
    dict.update([('name', name.get('name'))])  # Надо бы в бд занести
    dict.update([('surname', name.get('surname'))])
    dict.update([('coordinates', name.get('coordinates'))])
    return jsonify(dict)


@app.route("/all_workers", methods=['GET'])
def all_workers():
    out = []
    dict = {}
    cur.execute("SELECT* FROM workers")
    for row in cur:
        out.append(list(row))
    for i in range(len(out)):
        out_dict = {'name': out[i][1],
                    'surname': out[i][2]}
        dict.update([(out[i][0], out_dict)])
    return jsonify(dict)


""""
@app.route("/find_worker/<login>", methods=['GET'])
def find_worker_id(login):
    out = []
    dict = {}
    cur.execute("SELECT* FROM workers WHERE login = %(login)s", {'login': login})
    for row in cur:
        out.append(list(row))
    for i in range(len(out)):
        out_dict = {'name': out[i][1],
                    'surname': out[i][2]}
        dict.update([(out[i][0], out_dict)])
    return jsonify(dict)
"""


@app.route("/find_worker", methods=['POST'])
def find_worker_surname():
    surname = request.get_json()
    out = []
    dict = {}
    cur.execute("SELECT name, surname, lastname FROM workers WHERE surname "
                "= %(surname)s", {'surname': surname.get('surname')})
    for row in cur:
        out.append(list(row))
    for i in range(len(out)):
        out_dict = {'name': out[i][1],
                    'surname': out[i][2],
                    'lastname': out[i][3]}
        dict.update([(out[i][0], out_dict)])
    return jsonify(dict)


@app.route("/location", methods=['POST'])
def location():
    out = []
    dict = {}
    data = request.get_json()
    cur.execute("select* from workers inner join object_coordinates on object_coordinates.id_construction_object = "
                "workers.id_construction_object inner join shift on shift.login_worker = workers.login")
    for row in cur:
        out.append(list(row))
    shift_id = ''
    for i in range(len(out)):
        if str(out[i][0]).strip() == data.get('login') and str(out[i][14]).strip() == 'окончена':
            dict.update([('values_latitude', out[i][10][len(out[i][10]) - 1]),
                         ('values_longitude', out[i][12][len(out[i][12]) - 1])])
            return jsonify(dict)
        if str(out[i][0]).strip() == data.get('login') and str(out[i][14]).strip() == 'в процессе':
            shift_id = str(out[i][13]).strip()
            dict.update([('values_latitude', out[i][10][len(out[i][10]) - 1]),
                         ('values_longitude', out[i][12][len(out[i][12]) - 1])])
    cur.execute("select* from workers_coordinates where id_shift = %(id)s", {'id': shift_id})
    print(shift_id)
    for row in cur:
        dict.update([('coordinates_latitude', row[1][len(row[1]) - 1]),
                     ('coordinates_longitude', row[3][len(row[3]) - 1])])
        return jsonify(dict)


@app.route("/find_worker_android", methods=['GET'])
def find_worker_surname_android():
    surname = request.args
    out = []
    dict = {}
    cur.execute("SELECT name, surname, lastname FROM workers WHERE surname "
                "= %(surname)s", {'surname': surname.get('surname')})
    for row in cur:
        out.append(list(row))
    for i in range(len(out)):
        out_dict = {'name': out[i][1],
                    'surname': out[i][2],
                    'lastname': out[i][3]}
        dict.update([(out[i][0], out_dict)])
    return jsonify(dict)


@app.route("/all_workers_on_construction_object_without_status/<id>", methods=['GET'])
def all_workers_on_construction_object_without_status(id):
    out = []
    dict = {}
    cur.execute("select name, surname, lastname from workers where id_construction_object in"
                " (select  id from construction_object where id = %(id)s", {'id': id})
    for row in cur:
        out.append(list(row))
    for i in range(len(out)):
        out_dict = {'name': out[i][1],
                    'surname': out[i][2],
                    'lastname': out[i][3]}
        dict.update([(out[i][0], out_dict)])
    return jsonify(dict)


@app.route("/all_workers_on_construction_object/<id>", methods=['GET'])
def all_workers_on_construction_object(id):
    list_position = []
    cur.execute("select* from position")
    for row in cur:
        for i in range(len(row)):
            if i / 2 != 0:
                list_position.append(str(row[i]).strip())
    cur.execute(
        "select* from workers inner join shift on workers.login = shift.login_worker where id_construction_object = "
        "%(id)s", {'id': int(id)})
    out_list = []
    list_to_strip = []
    for row in cur:
        list_to_strip = []
        for i in range(len(row)):
            list_to_strip.append(str(row[i]).strip())
        out_list.append(list_to_strip)
    print(out_list)
    all_workers = {}
    index = 0
    for worker in out_list:
        worker_to_add = {}
        print(worker[4])
        worker_to_add.update([('login', worker[0]),
                              ('name', worker[1]),
                              ('surname', worker[2]),
                              ('lastname', worker[3]),
                              ('position', list_position[int(worker[4].strip())]),
                              ('status', worker[10]),
                              ('date', worker[12])])
        if all(worker_to_add['login'] != value['login'] for key, value in all_workers.items()):
            all_workers.update([(index, worker_to_add)])
            index += 1
        for key, value in all_workers.items():
            if value['login'] == worker_to_add['login'] and worker_to_add['status'] == 'в процессе':
                all_workers.update([(key, worker_to_add)])
    return jsonify(all_workers)


@app.route("/shift_start", methods=['POST'])
def shift_start():
    now = datetime.datetime.now()
    login = request.get_json()
    cur.execute("select id from shift")
    id_shift = 0
    for row in cur:
        id_shift += 1
    print(id_shift)
    cur.execute("insert into shift values(%(k)s, 'в процессе', %(login)s, %(date)s)",
                {'login': login.get('login'), 'k': id_shift, 'date': str(now).split()[0]})
    conn.commit()
    cur.execute("select* from workers_coordinates")
    k = 0
    for row in cur:
        k += 1
    print(k)
    cur.execute('insert into workers_coordinates values(%(id)s, %(first)s, %(id_shift)s)',
                {'id': k, 'first': None, 'id_shift': id_shift})
    conn.commit()
    dict = {'answer': 'success'}
    return jsonify(dict)


@app.route("/shift_start_android", methods=['GET'])
def shift_start_android():
    now = datetime.datetime.now()
    login = request.args
    cur.execute("select id from shift")
    id_shift = 0
    for row in cur:
        id_shift += 1
    print(id_shift)
    cur.execute("insert into shift values(%(k)s, 'в процессе', %(login)s, %(date)s)",
                {'login': login.get('login'), 'k': id_shift, 'date': str(now).split()[0]})
    conn.commit()
    cur.execute("select* from workers_coordinates")
    k = 0
    for row in cur:
        k += 1
    print(k)
    cur.execute('insert into workers_coordinates values(%(id)s, %(first)s, %(id_shift)s)',
                {'id': k, 'first': None, 'id_shift': id_shift})
    conn.commit()
    dict = {'answer': 'success'}
    return jsonify(dict)


@app.route("/shift_stop", methods=['POST'])
def shift_stop():
    login = request.get_json()
    cur.execute("update shift set status = 'окончена' where login_worker = %(login)s", {'login': login.get('login')})
    conn.commit()
    dict = {'answer': 'success'}
    return jsonify(dict)


@app.route("/shift_stop_android", methods=['GET'])
def shift_stop_android():
    login = request.args
    cur.execute("update shift set status = 'окончена' where login_worker = %(login)s", {'login': login.get('login')})
    conn.commit()
    dict = {'answer': 'success'}
    return jsonify(dict)


@app.route("/drop_down_list", methods=['GET'])
def drop_down_list():
    cur.execute("select* from position")
    position = [{}]
    i = 0
    for row in cur:
        position.append({})
        print(i)
        position[i].update([('id', row[0])])
        position[i].update([('position', str(row[1]).strip())])
        print(row[1])
        i += 1
    position.pop(i)
    cur.execute("select id, name from company")
    company = [{}]
    i = 0
    for row in cur:
        company.append({})
        company[i].update([('id', row[0]), ('company', str(row[1]).strip())])
        i += 1
    company.pop(i)
    out = {}
    out.update([('companies', company), ('positions', position)])
    return jsonify(out)


@app.route("/add_coordinates", methods=['POST'])
def add_coordinates():
    data = request.get_json()
    cur.execute("select id from shift where login_worker = %(login)s and status = 'в процессе'",
                {'login': data.get('login')})
    id = 0
    for row in cur:
        id = row[0]
        print(id)
    cur.execute("select coordinates_latitude from workers_coordinates where id_shift = %(id)s", {'id': id})
    k = 0
    try:
        for row in cur:
            k = len(row[0])
        print(k)
    except:
        k = 0
    print(data.get('coordinates_longitude'))
    print(data.get('coordinates_latitude'))
    cur.execute("update workers_coordinates set coordinates_latitude[%(k)s] = %(coordinates_latitude)s where id_shift "
                "= %(id)s",
                {'id': id, 'k': k, 'coordinates_latitude': data.get('coordinates_latitude')})
    conn.commit()
    cur.execute(
        "update workers_coordinates set coordinates_longitude[%(k)s] = %(coordinates_longitude)s where id_shift = %("
        "id)s",
        {'id': id, 'k': k, 'coordinates_longitude': data.get('coordinates_longitude')})
    conn.commit()
    dict = {'answer': 'success'}
    return jsonify(dict)


@app.route("/add_coordinates_android", methods=['GET'])
def add_coordinates_android():
    data = request.args
    cur.execute("select id from shift where login_worker = %(login)s and status = 'в процессе'",
                {'login': data.get('login')})
    id = 0
    for row in cur:
        id = row[0]
        print(id)
    cur.execute("select coordinates_latitude from workers_coordinates where id_shift = %(id)s", {'id': id})
    k = 0
    try:
        for row in cur:
            k = len(row[0])
        print(k)
    except:
        k = 0
    print(data.get('coordinates_longitude'))
    print(data.get('coordinates_latitude'))
    cur.execute("update workers_coordinates set coordinates_latitude[%(k)s] = %(coordinates_latitude)s where id_shift "
                "= %(id)s",
                {'id': id, 'k': k, 'coordinates_latitude': data.get('coordinates_latitude')})
    conn.commit()
    cur.execute(
        "update workers_coordinates set coordinates_longitude[%(k)s] = %(coordinates_longitude)s where id_shift = %("
        "id)s",
        {'id': id, 'k': k, 'coordinates_longitude': data.get('coordinates_longitude')})
    conn.commit()
    dict = {'answer': 'success'}
    return jsonify(dict)


# Поменять на ID устройства
@app.route("/add_coordinates/?coordinates_latitude", methods=['GET'])
def add_coordinates_arduino(device_number):
    data = request.get_json()
    cur.execute("select id from shift where device_number = %(device_number)s and status = 'в процессе'",
                {'device_number': device_number})
    id = 0
    for row in cur:
        id = row[0]
        print(id)
    cur.execute("select coordinates_latitude from workers_coordinates where id_shift = %(id)s", {'id': id})
    k = 0
    try:
        for row in cur:
            k = len(row[0])
        print(k)
    except:
        k = 0
    print(data.get('coordinates_longitude'))
    print(data.get('coordinates_latitude'))
    cur.execute("update workers_coordinates set coordinates_latitude[%(k)s] = %(coordinates_latitude)s where id_shift "
                "= %(id)s",
                {'id': id, 'k': k, 'coordinates_latitude': data.get('coordinates_latitude')})
    conn.commit()
    cur.execute(
        "update workers_coordinates set coordinates_longitude[%(k)s] = %(coordinates_longitude)s where id_shift = %("
        "id)s",
        {'id': id, 'k': k, 'coordinates_longitude': data.get('coordinates_longitude')})
    conn.commit()
    dict = {'answer': 'success'}
    return jsonify(dict)


@app.route("/company_registration", methods=['POST'])
def company_registration():
    try:
        print(request.get_json())
        name = request.get_json()
        cur.execute('select* from company')
        k = 0
        for row in cur:
            k += 1
        print(k)
        cur.execute("insert into company values(%(id)s, %(name)s, %(ogrn)s, %(inn)s, %(login)s, %(password)s)",
                    {'id': k,
                     'name': name.get('name'),
                     'ogrn': name.get('ogrn'),
                     'inn': name.get('inn'),
                     'login': name.get('login'),
                     'password': name.get('password')})
        conn.commit()
        dict = {'answer': 'success'}
        return jsonify(dict)
    except:
        dict = {'answer': 'fail'}
        return jsonify(dict)


@app.route("/company_registration_android", methods=['GET'])
def company_registration_android():
    try:
        name = request.args
        cur.execute('select* from company')
        k = 0
        for row in cur:
            k += 1
        print(k)
        cur.execute("insert into company values(%(id)s, %(name)s, %(ogrn)s, %(inn)s, %(login)s, %(password)s)",
                    {'id': k,
                     'name': name.get('name'),
                     'ogrn': name.get('ogrn'),
                     'inn': name.get('inn'),
                     'login': name.get('login'),
                     'password': name.get('password')})
        conn.commit()
        dict = {'answer': 'success'}
        return jsonify(dict)
    except:
        dict = {'answer': 'fail'}
        return jsonify(dict)


@app.route("/registration", methods=['POST'])
def registration():
    try:
        print(request.get_json())
        name = request.get_json()
        cur.execute('select id from position where name = %(position)s', {'position': name.get('position')})
        k = 0
        for row in cur:
            k = row[0]
        cur.execute(
            "INSERT INTO workers (login, name, surname, lastname, password, phone_number, id_position, device_number) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            ((name.get('login')),
             (name.get('name')),
             (name.get('surname')),
             (name.get('lastname')),
             (name.get('password')),
             (name.get('phone_number')),
             (k),
             (name.get('device_number'))))
        conn.commit()
        dict = {'answer': 'success'}
        return jsonify(dict)
    except:
        dict = {'answer': 'fail'}
        return jsonify(dict)


@app.route("/registration_android", methods=['GET'])
def registration_android():
    try:
        name = request.args
        cur.execute('select id from position where name = %(position)s', {'position': name.get('position')})
        k = 0
        for row in cur:
            k = row[0]
        cur.execute(
            "INSERT INTO workers (login, name, surname, lastname, password, phone_number, id_position, device_number) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            ((name.get('login')),
             (name.get('name')),
             (name.get('surname')),
             (name.get('lastname')),
             (name.get('password')),
             (name.get('phone_number')),
             (k),
             (name.get('device_number'))))
        conn.commit()
        dict = {'answer': 'success'}
        return jsonify(dict)
    except:
        dict = {'answer': 'fail'}
        return jsonify(dict)


@app.route("/authentication", methods=['POST'])
def authentication():
    try:
        print(request.get_json())
        data = request.get_json()
        cur.execute("select name, surname, lastname from workers where login = %(login)s and password = %(password)s",
                    {'login': data.get('login'),
                     'password': data.get('password')})
        out = []
        for row in cur:
            print(row)
            out.append(row)
        cur.execute('select status from shift where login_worker = %(login)s', {'login': data.get('login')})
        status = []
        for row in cur:
            print(row)
            status.append(row)
        if len(status) > 0:
            dict = {'answer': 'success', 'name': str(out[0][0]).strip(), 'surname': str(out[0][1]).strip(),
                    'lastname': str(out[0][2]).strip(), 'status': str(status[0]).strip()}
        else:
            dict = {'answer': 'success', 'name': str(out[0][0]).strip(), 'surname': str(out[0][1]).strip(),
                    'lastname': str(out[0][2]).strip(), 'status': 'окончена'}
        return jsonify(dict)
    except:
        dict = {'answer': 'fail'}
        return jsonify(dict)


@app.route("/authentication_android", methods=['GET'])
def authentication_android():
    try:
        data = request.args
        cur.execute("select name, surname, lastname from workers where login = %(login)s and password = %(password)s",
                    {'login': data.get('login'),
                     'password': data.get('password')})
        out = []
        for row in cur:
            print(row)
            out.append(row)
        cur.execute('select status from shift where login_worker = %(login)s', {'login': data.get('login')})
        status = []
        for row in cur:
            print(row)
            status.append(row)
        if len(status) > 0:
            dict = {'answer': 'success', 'name': str(out[0][0]).strip(), 'surname': str(out[0][1]).strip(),
                    'lastname': str(out[0][2]).strip(), 'status': str(status[0]).strip()}
        else:
            dict = {'answer': 'success', 'name': str(out[0][0]).strip(), 'surname': str(out[0][1]).strip(),
                    'lastname': str(out[0][2]).strip(), 'status': 'окончена'}
        return jsonify(dict)
    except:
        dict = {'answer': 'fail'}
        return jsonify(dict)


@app.route("/company_authentication", methods=['POST'])
def company_authentication():
    try:
        print(request.get_json())
        data = request.get_json()
        cur.execute("select name from company where login = %(login)s and password = %(password)s",
                    {'login': data.get('login'),
                     'password': data.get('password')})
        out = []
        for row in cur:
            out.append(row)
        dict = {'answer': 'success', 'name': str(out[0][0]).strip()}
        return jsonify(dict)
    except:
        dict = {'answer': 'fail'}
        return jsonify(dict)


@app.route("/company_authentication_android", methods=['GET'])
def company_authentication_android():
    try:
        data = request.args
        cur.execute("select name from company where login = %(login)s and password = %(password)s",
                    {'login': data.get('login'),
                     'password': data.get('password')})
        out = []
        for row in cur:
            out.append(row)
        dict = {'answer': 'success', 'name': str(out[0][0]).strip()}
        return jsonify(dict)
    except:
        dict = {'answer': 'fail'}
        return jsonify(dict)


@app.route("/statistics_1/<id>", methods=['GET'])
def statistics_1(id):
    plt.clf()
    list_position = []
    cur.execute("select* from position")
    for row in cur:
        for i in range(len(row)):
            if i / 2 != 0:
                list_position.append(str(row[i]).strip())
    print(list_position)
    cur.execute('select* from workers where id_construction_object = %(id)s', {'id': int(id)})
    workers = []
    for row in cur:
        print(row[4])
        workers.append(row[4])
    print(workers)
    for i in range(len(workers)):
        workers[i] = list_position[workers[i]]
    print(workers)
    positions = {}
    for position in set(workers):
        positions[position] = workers.count(position)

    data_names = []
    data_values = []
    for position in positions.keys():
        data_names.append(position)
        data_values.append(positions[position])
    print(data_values)
    print(data_names)
    dpi = 80
    fig = plt.figure(dpi=dpi, figsize=(512 / dpi, 384 / dpi))
    mpl.rcParams.update({'font.size': 9})

    plt.title('Распределение должностей на строительном объекте (%)')

    xs = range(len(data_names))

    plt.pie(
        data_values, autopct='%.1f', radius=1.1,
        explode=[0.15] + [0 for _ in range(len(data_names) - 1)])
    plt.legend(
        bbox_to_anchor=(-0.16, 0.45, 0.25, 0.25),
        loc='lower left', labels=data_names)
    fig.savefig('pie.png')
    return send_from_directory('D:\Учеба\Питон\pythonProject4', 'pie.png')


@app.route("/statistics_2/<id>", methods=['GET'])
def statistics_2(id):
    plt.clf()
    positions = []
    cur.execute("select* from position")
    position_name_bd = {}
    counts = []
    for row in cur:
        position_name_bd.update([(row[0], str(row[1]).strip())])
        positions.append(str(row[1]).strip())
        counts.append(0)
    print(position_name_bd)
    cur.execute('select* from workers inner join shift on workers.login = shift.login_worker inner join '
                'construction_object on Construction_object.id = workers.id_construction_object')

    for row in cur:
        counts[positions.index(position_name_bd[row[4]])] += 1

    print(counts)
    cur.execute('select* from company')
    company = ''
    for row in cur:
        print(row)
        if row[0] == id:
            company = str(row[1]).strip()
    plt.bar(positions, counts)
    plt.title(f"Количество рабочих смен компании '{company}'")
    plt.xlabel("Должность")
    plt.ylabel("Количество")
    plt.savefig('graph.png')
    return send_from_directory('D:\Учеба\Питон\pythonProject4', 'graph.png')


@app.route("/sos_signal", methods=['POST'])
def sos_signal():
    try:
        now = datetime.datetime.now()
        data = request.get_json()
        cur.execute('select* from workers where login = %(login)s', {'login': data.get('login')})
        k = 0
        for row in cur:
            print(row)
            k += 1
        if k == 0:
            dict = {'answer': 'fail'}
            return jsonify(dict)
        cur.execute('select* from sos_signal')
        k = 0
        for row in cur:
            k += 1
        cur.execute(
            "INSERT INTO sos_signal (login_worker, date, id) VALUES (%s, %s, %s)",
            ((data.get('login')),
             (str(now).split()[0]),
             (k)))
        conn.commit()
        dict = {'answer': 'success'}
        return jsonify(dict)
    except:
        dict = {'answer': 'fail'}
        return jsonify(dict)


@app.route("/sos_signal_android", methods=['GET'])
def sos_signal_android():
    try:
        now = datetime.datetime.now()
        data = request.args
        cur.execute('select* from workers where login = %(login)s', {'login': data.get('login')})
        k = 0
        for row in cur:
            print(row)
            k += 1
        if k == 0:
            dict = {'answer': 'fail'}
            return jsonify(dict)
        cur.execute('select* from sos_signal')
        k = 0
        for row in cur:
            k += 1
        cur.execute(
            "INSERT INTO sos_signal (login_worker, date, id) VALUES (%s, %s, %s)",
            ((dict.get('login')),
             (str(now).split()[0]),
             (k)))
        conn.commit()
        dict = {'answer': 'success'}
        return jsonify(dict)

    except:
        dict = {'answer': 'fail'}
        return jsonify(dict)


@app.route("/add_construction_object", methods=['POST'])  # Тут должно быть создание записи в таблице object_coordinates
def add_construction_object():
    print(request.get_json())
    data = request.get_json()
    cur.execute("select* from construction_object")
    k = 0
    for row in cur:
        k += 1
    print(k)
    cur.execute("insert into construction_object values(%(id)s, %(id_company)s, %(name)s)", {'id': k,
                                                                                             'id_company': data.get(
                                                                                                 'id'),
                                                                                             'name': data.get(
                                                                                                 'name')})
    conn.commit()
    cur.execute('select* from object_coordinates')
    f = 0
    for row in cur:
        f += 1
    cur.execute(
        'insert into object_coordinates values(%(k)s, %(coordinates_latitude)s, %(id)s, %(coordinated_longitude)s)', {
            'k': f,
            'coordinates_latitude': data.get('coordinates_latitude'),
            'id': k,
            'coordinated_longitude': data.get('coordinated_longitude')})
    conn.commit()
    dict = {'answer': 'success'}
    return jsonify(dict)


@app.route("/add_construction_object_android",
           methods=['GET'])  # Тут должно быть создание записи в таблице object_coordinates
def add_construction_object_android():
    data = request.args
    cur.execute("select* from construction_object")
    k = 0
    for row in cur:
        k += 1
    print(k)
    cur.execute("insert into construction_object values(%(id)s, %(id_company)s, %(name)s)", {'id': k,
                                                                                             'id_company': data.get(
                                                                                                 'id'),
                                                                                             'name': data.get(
                                                                                                 'name')})
    conn.commit()
    cur.execute('select* from object_coordinates')
    k = 0
    for row in cur:
        k += 1
    cur.execute(
        'insert into object_coordinates values(%(k)s, %(coordinates_latitude)s, %(id)s, %(coordinated_longitude)s)', {
            'k': k,
            'coordinates_latitude': data.get('coordinates_latitude'),
            'id': data.get('id'),
            'coordinated_longitude': data.get('coordinated_longitude')})
    conn.commit()
    dict = {'answer': 'success'}
    return jsonify(dict)  # @app.route("/<username>", methods=['GET'])


# def index(username):
#   return "Hello, %s!" % username


# @app.route('/', methods=['POST'])
# def add():
# f = request.get_json()
# return "Add the json request."


if __name__ == "__main__":
    app.run(debug=True)
