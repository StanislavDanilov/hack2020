import psycopg2
import datetime
import matplotlib

from flask import request, jsonify, app

conn = psycopg2.connect(database='hackathon', user='postgres', password='gennadi0', host='localhost', port=5432)
cur = conn.cursor()
def add_coordinates_check():
    data = {'login': 'dima', 'coordinates_latitude': 1234.1245, 'coordinates_longitude': 123.41255}
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
    cur.execute('select* from workers inner join object_coordinates on object_coordinates.id_construction_object = '
                'workers.id_construction_object')
    coord_lat = []
    coord_long = []
    for row in cur:
        print(row)
        if str(row[0]).strip() == data.get('login'):
            coord_lat = row[10]
            coord_long = row[12]
    print(coord_lat)
    print(coord_long)
    import matplotlib.path as mplPath
    import numpy as np
    bbPath = mplPath.Path(np.array([coord_lat[0], coord_long[0],
                                    [coord_lat[1], coord_long[1]],
                                    [coord_lat[2], coord_long[2]],
                                    [coord_lat[3], coord_long[3]]]))
    a = data.get('coordinates_latitude')
    b = data.get('coordinates_longitude')
    print(bbPath.contains_point((a, b)))

    dict = {'answer': 'success'}
    return dict


add_coordinates_check()
