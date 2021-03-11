import datetime
import gc
import os
import random
from io import BytesIO
from typing import Dict

import pandas as pd
import redis
import urllib3
from flask import Flask, render_template, json, request, send_file
from flask import jsonify
from flask_caching import Cache
from flask_selfdoc import Autodoc

from webdriver import fujian
from webdriver.brisbane import Brisbane
from controller.fujian_core import FujianCore

app = Flask(__name__)
auto = Autodoc(app)
host = os.environ['REDIS_HOST']
password = os.environ['REDIS_PASSWORD']

rediscon = redis.Redis(host=host,password=password, port=6379, db=7)

# GROUND ZERO ZONE
term = 2
EXCELMIME = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
app.config['RQ_ASYNC'] = True
app.config['RQ_CONNECTION_CLASS'] = 'redis.StrictRedis'
host = os.environ['REDIS_HOST']
password = os.environ['REDIS_PASSWORD']

cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_KEY_PREFIX': 'fujian_',
    'CACHE_REDIS_HOST': host,
    'CACHE_REDIS_PASSWORD': password,
    'CACHE_REDIS_PORT': '6379'})

studentcache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_KEY_PREFIX': 'fujian_student_',
    'CACHE_REDIS_HOST': host,
    'CACHE_REDIS_PASSWORD': password,
    'CACHE_REDIS_PORT': '6379',
    'CACHE_REDIS_DB': '5',
    'CACHE_DEFAULT_TIMEOUT': '86400'})


@app.route('/')
def hello_world():
    try:
        http = urllib3.PoolManager()
        http.request('GET', 'https://reg.sut.ac.th/registrar')
        message = "Everything's Gonna be OK!"
        return render_template('landing.html', msg=message)
    except:
        message = 'SUT Registrar System Unavailable'
        return render_template('landing.html', msg=message)


@app.route('/student/<student_id>', methods=['POST'])
@auto.doc()
def getStudentEnroll(student_id):
    fujian = FujianCore(student_id)
    data = fujian.getStudentInfo()
    redis_data = cache.get(student_id)
    if redis_data is None:
        cache.set(student_id, data)
        return jsonify(data)
    else:
        return jsonify(redis_data)


@app.route('/student/<student_id>/<int:eduyear>', methods=['POST'])
@auto.doc()
def getStudentEnroll_EDUYEAR(student_id, eduyear):
    fujian = FujianCore(student_id, eduyear)
    data = fujian.getStudentInfo()
    redis_data = cache.get(str(student_id) + '_eduyear_' + str(eduyear))
    if redis_data is None:
        cache.set(str(student_id) + '_eduyear_' + str(eduyear), data)
        return jsonify(data)
    else:
        return jsonify(redis_data)


@app.route('/student/<student_id>/<int:eduyear>/<int:term>', methods=['POST'])
@auto.doc()
def getStudentEnroll_EDUYEAR_TERM(student_id, eduyear, term) -> json:
    fujian = FujianCore(student_id, eduyear, term)
    data = fujian.getStudentInfo()

    redis_data = cache.get(str(student_id) + '_eduyear_' + str(eduyear) + '_term_' + str(term))
    if redis_data is None:
        cache.set(str(student_id) + '_eduyear_' + str(eduyear) + '_term_' + str(term), data)
        return jsonify(data)
    else:
        return jsonify(redis_data)


@app.route('/student/<student_id>', methods=['GET'])
# @cache.cached(timeout=(60 * 5))
def getStudentHTML(student_id):
    fujian = FujianCore(student_id)
    data = fujian.getStudentInfo()

    images_file = []
    for filename in os.listdir('static/img/tech'):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            images_file.append(os.path.join('img/tech', filename))
        else:
            continue
    return render_template('student.html',
                           degree=data['degree'],
                           yr=data['graduated_for'],
                           lensub=len(data['enroll_subjects']),
                           subject_id=data['enroll_subjects'],
                           subject_name=data['enroll_subjects_name'],
                           student_name=data['student_name'],
                           student_id=student_id,
                           institute=data['institute'],
                           minor=data['minor'],
                           assistant=data['assistant'], images_file=images_file)


@app.route('/subject/<subject_id>', methods=['GET'])
def getOnlineSubject(subject_id):
    subject = fujian.getonline_subject(subject_id[:6])
    return jsonify(subject)


# @app.errorhandler(Exception)
# def handle_exception(e):
#     # error_link = ['https://www.youtube.com/embed/7Hvkhh4GaI0?controls=0&autoplay=1',
#     #               'https://www.youtube.com/embed/PFygXz-Y0zA?controls=0&autoplay=1',
#     #               'https://www.youtube.com/embed/wpHlagmXzxY?controls=0&autoplay=1',
#     #               'https://www.youtube.com/embed/v5aepf1t5CU?controls=0&autoplay=1',
#     #               'https://www.youtube.com/embed/u06GqlNiJUY?controls=0&autoplay=1',
#     #               'https://www.youtube.com/embed/ztxs6nixsaI?controls=0&autoplay=1',
#     #               'https://www.youtube.com/embed/1iqd-AL6soE?controls=0&autoplay=1',
#     #               'https://www.youtube.com/embed/-OAPdG8sgLs?controls=0&autoplay=1&start=166',
#     #               'https://www.youtube.com/embed/0GFKs17cjWs?controls=0&autoplay=1',
#     #               'https://www.youtube.com/embed/pAP9qcjPvtE?controls=0&autoplay=1',
#     #               'https://www.youtube.com/embed/k2CXu4K40bg?controls=0&autoplay=1',
#     #               'https://www.youtube.com/embed/hmj-RT3S-d4?controls=0&autoplay=1&start=5',
#     #               'https://www.youtube.com/embed/0QYGWXEXZwU?controls=0&autoplay=1']
#     error_link = ['https://www.youtube.com/embed/IFcUBch8VNY?controls=0&autoplay=1']
#     rd = random.randint(0, len(error_link) - 1)
#     error_random = random.randint(100, 600)
#     error_random_minus = random.randint(random.randint(1, 5), random.randint(10, 20))
#     return render_template('error.html', error_link=error_link[rd], log=e,
#                            error_code=error_random), error_random - error_random_minus


def botGetStudent(student_id):
    fujian = FujianCore(student_id)
    data = fujian.getStudentInfo()

    redis_data = cache.get(student_id)
    gc.collect()
    if redis_data is None:
        cache.set(student_id, data)
        return data
    else:
        return redis_data


@app.route('/chatbot/webhook', methods=['POST'])
def webhook() -> Dict:
    response_body = []
    payload = {}
    request_body = request.get_json(force=True)
    params = request_body['queryResult']['parameters']
    if 'student_id' in params:
        info = botGetStudent(str(params['student_id']).upper())
        loop = 0
        for subject in info['enroll_subjects']:
            response_body.append({
                "type": "text",
                "text": "รายวิชาที่ " + str(loop + 1) + " " + str(subject) + " | " + str(
                    info['enroll_subjects_name'][loop]),
                "weight": "regular",
                "size": "sm",
                "align": "center",
                "style": "normal",
                "contents": []
            })
            loop = loop + 1

        linedata = {
            "line": {
                "type": "flex",
                "altText": "ข้อมูลรายวิชาของ " + str(params['student_id']),
                "contents": {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "รายวิชาของนักศึกษารหัส " + info['student_id'],
                                "weight": "bold",
                                "size": "sm",
                                "gravity": "center",
                                "contents": []
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "margin": "lg",
                                "contents": [
                                    {
                                        "type": "box",
                                        "layout": "baseline",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": "ชื่อ - นามสกุล",
                                                "size": "sm",
                                                "color": "#AAAAAA",
                                                "contents": []
                                            },
                                            {
                                                "type": "text",
                                                "text": info['student_name'],
                                                "size": "sm",
                                                "color": "#666666",
                                                "contents": []
                                            }
                                        ]
                                    },
                                    {
                                        "type": "box",
                                        "layout": "baseline",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": "สำนักวิชา",
                                                "size": "sm",
                                                "color": "#AAAAAA",
                                                "contents": []
                                            },
                                            {
                                                "type": "text",
                                                "text": info['institute'],
                                                "size": "sm",
                                                "color": "#666666",
                                                "contents": []
                                            }
                                        ]
                                    },
                                    {
                                        "type": "box",
                                        "layout": "baseline",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": "สาขาวิชา",
                                                "size": "sm",
                                                "color": "#AAAAAA",
                                                "contents": []
                                            },
                                            {
                                                "type": "text",
                                                "text": info['minor'],
                                                "size": "sm",
                                                "color": "#666666",
                                                "contents": []
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "margin": "xxl",
                                "contents": [
                                    {
                                        "type": "spacer"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": response_body
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
        }
        payload.update(linedata)
    elif 'person' in params:
        redis_data = studentcache.get('info_term_count_' + str(term))
        gc.collect()
        stdc = redis_data

        linedata_student_count = {
            "line": {
                "type": "flex",
                "altText": "จำนวนนักศึกษา",
                "contents": {
                    "type": "bubble",
                    "hero": {
                        "type": "image",
                        "url": "https://cloud.arsanandha.xyz/static/img/header/fujianog.png",
                        "align": "center",
                        "size": "full",
                        "aspectRatio": "20:13",
                        "aspectMode": "cover",
                        "action": {
                            "type": "uri",
                            "label": "Action",
                            "uri": "https://cloud.arsanandha.xyz/"
                        }
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "md",
                        "contents": [
                            {
                                "type": "text",
                                "text": "จำนวนนักศึกษา มทส. ในเทอมนี้",
                                "weight": "bold",
                                "size": "sm",
                                "align": "center",
                                "gravity": "center",
                                "contents": []
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "spacing": "sm",
                                "margin": "lg",
                                "contents": [
                                    {
                                        "type": "box",
                                        "layout": "baseline",
                                        "spacing": "sm",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": str(stdc),
                                                "size": "3xl",
                                                "color": "#FF5700FF",
                                                "align": "center",
                                                "gravity": "center",
                                                "contents": []
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "button",
                                        "action": {
                                            "type": "uri",
                                            "label": "ไฟล์รายชื่อ นศ",
                                            "uri": "https://cloud.arsanandha.xyz/getExcel"
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
        }
        payload.update(linedata_student_count)

    response = app.response_class(
        response=json.dumps({
            "fulfillmentMessages": [
                {
                    "payload": payload,
                    "platform": "LINE"
                }
            ]
        }, sort_keys=False),
        mimetype='application/json'
    )
    return response


@app.route('/documentation')
def documentation():
    return auto.html(
        template='customdoc.html',
        title='Fujian Documentation',
        author='ARSANANDHA+',
        content=auto.generate()
    )


@app.route('/getstudent', methods=['GET'])
def getStudentQueue():
    bx = Brisbane(2563, term, 1, 3, 'get_student')
    redis_data = studentcache.get('info_term_' + str(term))
    gc.collect()
    if redis_data is None:
        data = bx.get_student_info()
        studentcache.set('info_term_' + str(term), data)
        studentcache.set('info_term_count_' + str(term), len(data))
        return render_template('student_count.html',student_count=len(data))
    else:
        return render_template('student_count.html',student_count=len(redis_data))


@app.route('/getExcel', methods=['GET'])
def getExcelFile():
    redis_data = studentcache.get('info_term_' + str(term))
    f = []

    for rs in redis_data:
        f.append(json.loads(rs))

    output = BytesIO()
    df = pd.DataFrame(f)
    df.index += 1
    df.to_excel(output, sheet_name='Student at Term ' + str(term))
    output.seek(0)

    return send_file(output,
                     attachment_filename='student_term_' + str(term) + '.xlsx',
                     as_attachment=True,
                     mimetype=EXCELMIME)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
