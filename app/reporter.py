# from flask import Blueprint, jsonify, request
import math
import sys
import click
import json
import os
import re
import numpy
import time
from datetime import datetime, timedelta
import pandas as pd
import requests
from flask import Blueprint
from app import db
from app.models import TermC, TermCT, TagC, TagCT, TagRelateC, TagRelateCT, TopicC, TopicCT, ThreadC, ThreadCT, \
    ResourceRelateCT, ResourceRelateC, ResourceC, ResourceCT, ThreadRelateC, ThreadRelateCT, TopicRelateC, \
    TopicRelateCT, AuthorCT, AuthorC, AuthorRelateCT, AuthorRelateC, ObjectCT, ObjectC, ObjectRelateC, ObjectRelateCT, TermRelateCT, TermRelateC

bd = Blueprint('reporter', __name__)


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


@bd.cli.command('list')
@click.argument('cat')
def buildLst(cat):
    try:
        if cat == 'ttc':
            tit = "Tuoi Tre Cuoi"
            top = TopicC.query.count()
            cat = TermC.query.count()
            thread = ThreadC.query.count()
            tag = TagC.query.count()
            resource = ResourceC.query.count()
            author = AuthorC.query.count()
            obj = ObjectC.query.count()
        else:
            tit = "Tuoi Tre Cuoi tuan"
            top = TopicCT.query.count()
            cat = TermCT.query.count()
            thread = ThreadCT.query.count()
            tag = TagCT.query.count()
            resource = ResourceCT.query.count()
            author = AuthorCT.query.count()
            obj = ObjectCT.query.count()
        print("[m] ========================== %s ==========================" % tit)
        print("[m] Chuyen muc : %d" % cat)
        print("[m] Chu de : %d" % top)
        print("[m] Chuyen de : %d" % thread)
        print("[m] Tu khoa : %d" % tag)
        print("[m] Tac gia : %d" % author)
        print("[m] Tai nguyen : %d" % resource)
        print("[m] Tin bai : %d" % obj)
        print("[m] ==========================================================")
    except Exception as e:
        print(" [x] Fail")
        tb = sys.exc_info()[2]
        raise e.with_traceback(tb)