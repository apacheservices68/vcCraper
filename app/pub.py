import re
import os
import sys
import json
import pika
import time
import click
import requests
import pandas as pd
from datetime import datetime, timedelta
from flask import Blueprint, jsonify

pub = Blueprint('dll', __name__)


########################
def getRngByNum(pers):
    tmpRng = pd.date_range(end=datetime.today(), periods=int(pers)).to_pydatetime()  # range date
    to = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    fr = datetime.strftime(tmpRng[0], "%Y-%m-%d %H:%M:%S")
    return dict(fr=fr, to=to)


########################
def getRngByInp(fr, to):
    fr = pd.to_datetime(fr, format='%Y-%m-%d')
    to = pd.to_datetime(to, format='%Y-%m-%d')
    fr = fr.strftime("%Y-%m-%d %H:%M:%S")
    to = to.strftime("%Y-%m-%d %H:%M:%S")
    return dict(fr=fr, to=to)


# Convert from to date to readable collection params
#########################
def getFrToPam(fr, to):
    try:
        int(fr)
        isIn = True
    except ValueError:
        isIn = False
    if not isIn:
        tmp = getRngByInp(fr, to)
    else:
        tmp = getRngByNum(fr)
    return tmp


##########################
def splitToChunks(list_a, chunk_size):
    for i in range(0, len(list_a), chunk_size):
        yield list_a[i:i + chunk_size]


###########################
def getLst(cat, size, fr, to):
    api_url = os.environ.get('MAIN_API') + '/sharelistnews'
    myobj = {
        "seckey": os.environ.get('seckey'),
        "catid": cat,
        "size": size,
        "page": 0,
        'order': 'desc',
        "frdate": fr,
        "todate": to,
    }
    response = requests.post(api_url, data=myobj)
    json_response = json.loads(response.text)
    json_response = json_response[::-1]
    return json_response


def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError as e:
        return False
    return True


def unique(list1):
    # initialize a null list
    unique_list = []

    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    return unique_list


def toTimestamp(str):
    if str.find('.') == -1:
        return round(time.mktime(datetime.strptime(str, "%Y-%m-%dT%H:%M:%S").timetuple()))
    else:
        return round(time.mktime(datetime.strptime(str, "%Y-%m-%dT%H:%M:%S.%f").timetuple()))


########################### Get resource from api #############################
@pub.cli.command('get')
@click.argument('cat')
@click.argument('size')
@click.argument('fr')
@click.argument('to')
def get(cat, size, fr, to):
    try:
        print("====================================================================================")
        range = getFrToPam(fr, to)
        json_response = getLst(cat, size, range['fr'], range['to'])
        valueList = []
        for idx, val in enumerate(json_response):
            listAvatar = [
                val['Avatar'],
                val['Avatar2'],
                val['Avatar3'],
                val['Avatar4']
            ]
            if val['Avatar5'] is not None and is_json(val['Avatar5']):
                collectionAvatar = json.loads(val['Avatar5'])
                for i, v in enumerate(collectionAvatar):
                    listAvatar.append(collectionAvatar[v])

            for v in listAvatar:
                if v is not None and v != "":
                    v = re.sub(r"^(.*tuoitre\.vn|tuoitre)", "", v)
                    # v = "/" + v
                    valueList.append(v)
            ######################
            regex = r"([\/\w+.])+([\/\d+.])+([\w\s_\\.\-\(\):])+(.jpg|.mp4|.jpeg|.gif|.mpg|.mp3|.mov|.wav|.m4a)"
            matches = re.finditer(regex, val['Body'], re.MULTILINE)
            for matchNum, match in enumerate(matches, start=1):
                tmp = match.group()
                tmp = re.sub(r"(.*cdn.tuoitre.vn|.*static.tuoitre.vn|.*thumbs.*.vn|tuoitre)(.*)(\/\d{4}\/\d{1,2}\/\d{1,"
                             r"2}\/([\w\s_\\.\-\(\):])+(.jpg|.mp4|.jpeg|.gif|.mpg|.mp3|.mov|.wav|.m4a))", r"\2\3",
                             tmp)  ## Version 2
                tmp = re.sub(r"\s", r"%20", tmp)
                valueList.append(tmp)
        ### Remove duplicate dict from list
        valueList = unique(valueList)
        newValueList = []
        for i, v in enumerate(purify(valueList)):
            # file = getFullUrl(v)
            regex = r"((.*)(\/\d{4}\/\d{1,2}\/\d{1,2}\/)(([\w\s_\\.\-\(\):])+(" \
                    r".jpg|.mp4|.jpeg|.gif|.mpg|.mp3|.mov|.wav|.m4a)))"
            test_str = re.sub(r"\/\/", r"/", "/" + v)
            matches = re.finditer(regex, test_str, re.MULTILINE)
            for matchNum, match in enumerate(matches, start=1):
                tmp = dict(Domain=getDomain(v), Path=match.group(2) + match.group(3), Filename=match.group(4))
                sender(getDomain(v), match.group(2) + match.group(3), match.group(4), cat)
                #break
                # print(saveTo(tmp, cat))
                # newValueList.append(tmp)
        # print(newValueList)

    except Exception as e:
        print(" [x] Fail")
        tb = sys.exc_info()[2]
        print(e.with_traceback(tb))


def sender(domain, path, filename, cat):
    try:
        url = os.environ.get('CLOUDAMQP_URL')
        parameters = pika.URLParameters(url)
        parameters.socket_timeout = 5
        queueName = "download_queue"
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        dataReady = [domain, path, filename, cat]
        separator = ','
        channel.queue_declare(queue=queueName, durable=True)
        msg = separator.join(dataReady)
        channel.queue_declare(queue=queueName, durable=True)
        # message = bytes(separator)
        channel.basic_publish(
            exchange='',
            routing_key=queueName,
            body=msg,
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
        print(" [x] Sent %r" % msg)
        connection.close()
        return jsonify(
            status=200,
            message="[m] Save " + filename + " !"
        )
    except Exception as e:
        print(e)
        return jsonify(
            status=400,
            message="Save false"
        )


def saveTo(infos, cat):
    url = infos['Domain'] + infos['Path'] + infos['Filename']
    path = re.sub(r"\/\/", r"/", os.environ.get("RESOURCE_PATH") + cat + infos['Path'])
    filePath = path + infos['Filename']
    CHECK_FOLDER = os.path.isdir(path)
    # If folder doesn't exist, then create it.
    if not CHECK_FOLDER:
        os.makedirs(path, mode=0o755, exist_ok=False)
        print("[m] Created folder : ", path)
    r = requests.get(url, stream=True)
    if r.status_code != 200:
        print("[m] Url does not exist - ", url)
    with open(filePath, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)


def urlCode(url):
    try:
        response = requests.head(url, allow_redirects=False)
        return response.status_code
    except Exception as e:
        print(f'[ERROR]: {e}')


@pub.cli.command('db')
@click.argument('type')
@click.argument('order')
def get(type, order):
    try:
        print("====================================================================================")
        print(type, order)
    except Exception as e:
        print(" [x] Fail")
        tb = sys.exc_info()[2]
        print(e.with_traceback(tb))


def purify(valueList):
    newValueList = []
    for i, v in enumerate(valueList):
        if os.path.isfile(v):
            continue
        test = re.sub(
            r"(.*)(\/\d{4}\/\d{1,2}\/\d{1,2}\/([\w\s_\\.\-\(\):])+(.jpg|.mp4|.jpeg|.gif|.mpg|.mp3|.mov|.wav|.m4a))",
            r"\2", v)
        if v not in newValueList:
            newValueList.append(v)
        ##
        x = re.search("^\/tuoitre.*$", v)
        if x:
            continue
        if (test == v) == False:
            if test not in newValueList:
                newValueList.append(test)
    return newValueList


def getDomain(path):
    domain = os.environ.get("CDN_DOMAIN")
    x = re.search("^\/tuoitre.*$", path)
    if x:
        domain = os.environ.get("THUMBS_DOMAIN")
    y = re.search("^.*mp3$", path)
    if y:
        domain = os.environ.get("STATIC_DOMAIN")
    return domain


def getFileName(path):
    ## Replace whitespace
    domain = os.environ.get("CDN_DOMAIN")
    x = re.search("^\/tuoitre.*$", path)
    if x:
        domain = os.environ.get("THUMBS_DOMAIN")
    y = re.search("^.*mp3$", path)
    if y:
        domain = os.environ.get("STATIC_DOMAIN")
    path = re.sub(r"^\/+", r"", path)
    path = re.sub(r"\/+", r"/", path)
    return domain + "/" + path

# def add():
#     url = "amqp://zyz:zyz123@@localhost:5672/%2f"
#     parameters = pika.URLParameters(url)
#     parameters.socket_timeout = 5
#     connection = pika.BlockingConnection(parameters)
#     channel = connection.channel()
#     channel.queue_declare(queue='task_queue', durable=True)
#     if request.method == 'POST':
#         try:
#             data=validate()
#             sbd = data['sbd']
#             email = data['email']
#             prefix = data['prefix']
#             numList = [sbd,email,prefix]
#             separator = ','
#             channel.queue_declare(queue='task_queue', durable=True)
#             # message = ' '.join(sys.argv[1:]) or "bbb!"
#             message = separator.join(numList)
#             channel.basic_publish(
#                 exchange='',
#                 routing_key='task_queue',
#                 body=message,
#                 properties=pika.BasicProperties(
#                     delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
#                 ))
#             # print(" [x] Sent %r" % message)
#             connection.close()
#             return jsonify(
#                 status=200,
#                 message="Save success!"
#             )
#         except Exception as e:
#             print(e)
#             return jsonify(
#                 status=400,
#                 message="Save false"
#             )
