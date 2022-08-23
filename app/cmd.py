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
    TopicRelateCT, AuthorCT, AuthorC, AuthorRelateCT, AuthorRelateC, ObjectCT, ObjectC

bd = Blueprint('import', __name__)


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
@click.argument('size')
@click.argument('fr')
@click.argument('to')
def buildLst(cat, size, fr, to):
    try:
        api_url = os.environ.get('MAIN_API') + '/sharelistnews'
        range = getFrToPam(fr, to)
        myobj = {
            "seckey": os.environ.get('seckey'),
            "catid": cat,
            "size": size,
            "page": 0,
            "frdate": range["fr"],
            "todate": range["to"],
            # "order": "desc"
        }
        response = requests.post(api_url, data=myobj)
        json_response = json.loads(response.text)
        # json_response = json_response[::-1]
        for idx, val in enumerate(json_response):
            parse = json.loads(val['Tag'])
            # print(parse[0])
            print(val['Title'], val['LastModifiedDate'])
            # directUrl = os.environ.get('MAIN_DOMAIN') + val['OriginalUrl']
            # webbrowser.open_new_tab(directUrl)
        # url = json_response[100]['Domain']
        # browser.open_new_tab(photo_url)
        print("DEMO done!")
    except Exception as e:
        print(e)


@bd.cli.command('tag')
@click.argument('type')
@click.argument('cat')
@click.argument('size')
@click.argument('fr')
@click.argument('to')
def buildTag(type, cat, size, fr, to):
    try:
        api_url = os.environ.get('MAIN_API') + '/sharelistnews'
        range = getFrToPam(fr, to)
        myobj = {
            "seckey": os.environ.get('seckey'),
            "catid": cat,
            "size": size,
            "page": 0,
            "frdate": range["fr"],
            "todate": range["to"],
        }
        response = requests.post(api_url, data=myobj)
        json_response = json.loads(response.text)
        tagValueList = []
        for idx, val in enumerate(json_response):
            # print(val['NewsId'], val['Title'])
            #################### Tag Handler #####################
            if val['Tag'] != "":
                parse = json.loads(val['Tag'])
                for i, v in enumerate(parse):
                    tmp = dict(PartnerId=v['Id'], Name=v['Name'], Url=v['Url'])
                    if type == 'ttc':
                        q = TagC.query.filter_by(Url=v['Url'], PartnerId=v['Id']).first()
                    else:
                        q = TagCT.query.filter_by(Url=v['Url'], PartnerId=v['Id']).first()
                    if q is not None:
                        continue
                    tagValueList.append(tmp)
        ### Remove duplicate dict from list
        result = []
        for i in tagValueList:
            if i not in result:
                result.append(i)
        ### Calculate size of results
        default = int(os.environ.get('CHUNK_SIZE'))
        size = math.ceil(len(result) / default)
        chunker = numpy.array_split(result, size)
        counter = 0
        ### Insert list of dict to database
        for i, v in enumerate(chunker):
            print("[m] Step %d \n [m]Total %d\n", i, len(v))
            if type == 'ttc':
                db.session.bulk_insert_mappings(TagC, v)
            else:
                db.session.bulk_insert_mappings(TagCT, v)
        db.session.commit()
        print("[m] Inserted tag done.")
    except Exception as e:
        print(e)


@bd.cli.command('tag-relate')
@click.argument('type')
@click.argument('cat')
@click.argument('size')
@click.argument('fr')
@click.argument('to')
def buildTagRelate(type, cat, size, fr, to):
    try:
        api_url = os.environ.get('MAIN_API') + '/sharelistnews'
        range = getFrToPam(fr, to)
        myobj = {
            "seckey": os.environ.get('seckey'),
            "catid": cat,
            "size": size,
            "page": 0,
            "frdate": range["fr"],
            "todate": range["to"],
        }
        response = requests.post(api_url, data=myobj)
        json_response = json.loads(response.text)
        print(len(json_response))
        tagValueList = []
        for idx, val in enumerate(json_response):
            #################### Tag Handler #####################
            if val['Tag'] != "":
                parse = json.loads(val['Tag'])
                for i, v in enumerate(parse):
                    tmp = dict(PartnerId=v['Id'], ArticleId=val['NewsId'], Url=v['Url'])
                    if type == 'ttc':
                        q = TagRelateC.query.filter_by(Url=v['Url'], ArticleId=val['NewsId']).all()
                    else:
                        q = TagRelateCT.query.filter_by(Url=v['Url'], ArticleId=val['NewsId']).all()
                    ### Delete old relationship
                    if q:
                        for qi, qv in enumerate(q):
                            db.session.delete(q[qi])
                        db.session.commit()
                    tagValueList.append(tmp)
        ### Remove duplicate dict from list
        result = []
        for i in tagValueList:
            if i not in result:
                result.append(i)
        ### Calculate size of results
        default = int(os.environ.get('CHUNK_SIZE'))
        size = math.ceil(len(result) / default)
        chunker = numpy.array_split(result, size)
        counter = 0
        ### Insert list of dict to database
        for i, v in enumerate(chunker):
            print("[m] Step %d \n[m]Total %d\n" % (i, len(v)))
            if type == 'ttc':
                db.session.bulk_insert_mappings(TagRelateC, v)
            else:
                db.session.bulk_insert_mappings(TagRelateCT, v)
        db.session.commit()
        print("[m] Inserted tag done.")
    except Exception as e:
        print(e)


@bd.cli.command('resources')
@click.argument('cat')
@click.argument('size')
@click.argument('fr')
@click.argument('to')
def buildResources(cat, size, fr, to):
    try:
        range = getFrToPam(fr, to)
        json_response = getLst(cat, size, range['fr'], range['to'])
        valueList = []
        # replList = ["//cdn.tuoitre.vn", "tuoitre","https\:\/\/cdn.tuoitre.vn"]
        for idx, val in enumerate(json_response):

            ### Handle avatar ###
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
                # tmp = re.sub(r"^(.*tuoitre\.vn|tuoitre)", "", tmp)
                # tmp = re.sub(r"(.*)(\/\d{4}\/\d{1,2}\/\d{1,2}\/([\w\s_\\.\-\(\):])+(.jpg|.mp4|.jpeg|.gif))", r"\2", tmp) ## Version 1
                tmp = re.sub(r"(.*cdn.tuoitre.vn|.*static.tuoitre.vn|tuoitre)(.*)(\/\d{4}\/\d{1,2}\/\d{1,"
                             r"2}\/([\w\s_\\.\-\(\):])+(.jpg|.mp4|.jpeg|.gif|.mpg|.mp3|.mov|.wav|.m4a))", r"\2\3",
                             tmp)  ## Version 2
                valueList.append(tmp)
                # print("Match {match}".format(match=match.group()))
                # for groupNum in range(0, len(match.groups())):
                #     groupNum = groupNum + 1
                #
                #     print("Group {groupNum} found at {start}-{end}: {group}".format(groupNum=groupNum,
                #                                                                     start=match.start(groupNum),
                #                                                                     end=match.end(groupNum),
                #                                                                     group=match.group(groupNum)))
            # print("\n")
        ### Remove duplicate dict from list
        valueList = unique(valueList)
        result = []
        for i in valueList:
            i = re.sub(r"[\/]{2,}", "/", i)
            if os.path.isfile(i):
                continue
            if cat == 'ttc':
                q = ResourceC.query.filter_by(Path=i).first()
            else:
                q = ResourceCT.query.filter_by(Path=i).first()
            if q is not None:
                continue
            i = i.strip()  ## whitespace
            if i == "" and len(i) > 250:
                continue

            tmp = dict(Path=i)
            result.append(tmp)
        ### Insert list of dict to database
        if len(result) == 0:
            print("[m] No one.")
            exit()
        default = int(os.environ.get('CHUNK_SIZE'))
        size = math.ceil(len(result) / default)
        chunker = numpy.array_split(result, size)
        ### Insert list of dict to database
        for i, v in enumerate(chunker):
            print("[m] Step %d \n[m] Total %d items inserted" % (i, len(v)))
            if cat == 'ttc':
                db.session.bulk_insert_mappings(ResourceC, v)
            else:
                db.session.bulk_insert_mappings(ResourceCT, v)
        db.session.commit()
        print("[m] Inserted resources done.")
    except Exception as e:
        tb = sys.exc_info()[2]
        print(e.with_traceback(tb))
        db.session.rollback()
        print(" [x] Fail")


@bd.cli.command('resource-relate')
@click.argument('cat')
@click.argument('size')
@click.argument('fr')
@click.argument('to')
def buildResourceRelate(cat, size, fr, to):
    try:
        range = getFrToPam(fr, to)
        json_response = getLst(cat, size, range['fr'], range['to'])
        result = []
        # replList = ["//cdn.tuoitre.vn", "tuoitre","https\:\/\/cdn.tuoitre.vn"]
        for idx, val in enumerate(json_response):
            valueList = []
            ### Handle avatar ###
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

            ### Handle Content ###
            regex = r"([\/\w+.])+([\/\d+.])+([\w\s_\\.\-\(\):])+(.jpg|.mp4|.jpeg|.gif|.mpg|.mp3|.mov|.wav|.m4a)"
            matches = re.finditer(regex, val['Body'], re.MULTILINE)
            for matchNum, match in enumerate(matches, start=1):
                tmp = match.group()
                # tmp = re.sub(r"^(.*tuoitre\.vn|tuoitre)", "", tmp)
                # tmp = re.sub(r"(.*)(\/\d{4}\/\d{1,2}\/\d{1,2}\/([\w\s_\\.\-\(\):])+(.jpg|.mp4|.jpeg|.gif))", r"\2", tmp) ## Version 1
                tmp = re.sub(r"(.*cdn.tuoitre.vn|.*static.tuoitre.vn|tuoitre)(.*)(\/\d{4}\/\d{1,2}\/\d{1,"
                             r"2}\/([\w\s_\\.\-\(\):])+(.jpg|.mp4|.jpeg|.gif|.mpg|.mp3|.mov|.wav|.m4a))", r"\2\3",
                             tmp)  ## Version 2
                valueList.append(tmp)
                # print("Match {match}".format(match=match.group()))
                # for groupNum in range(0, len(match.groups())):
                #     groupNum = groupNum + 1
                #
                #     print("Group {groupNum} found at {start}-{end}: {group}".format(groupNum=groupNum,
                #                                                                     start=match.start(groupNum),
                #                                                                     end=match.end(groupNum),
                #                                                                     group=match.group(groupNum)))
            ### Remove duplicate value
            valueList = unique(valueList)
            ### Delete old Relationship
            if cat == 'ttc':
                q = ResourceRelateC.query.filter_by(ArticleId=val['NewsId']).all()
            else:
                q = ResourceRelateCT.query.filter_by(ArticleId=val['NewsId']).all()
            if q:
                for qi, qv in enumerate(q):
                    db.session.delete(q[qi])
                db.session.commit()
            ### Create new dict data
            for i, v in enumerate(valueList):
                v = re.sub(r"[\/]{2,}", "/", v)
                if os.path.isfile(v):
                    continue
                v = v.strip()  ## whitespace
                if v == "" and len(v) > 250:
                    continue
                t = dict(ArticleId=val['NewsId'], ExtraParams=None, Path=v)
                result.append(t)
        # print(result)

        ######################
        # print("\n")
        ### Remove duplicate dict from list
        # valueList = unique(valueList)
        # result = []
        # for i in valueList:
        #     i = re.sub(r"[\/]{2,}", "/", i)
        #     if os.path.isfile(i):
        #         continue
        #     if cat == 'ttc':
        #         q = ResourceC.query.filter_by(Path=i).first()
        #     else:
        #         q = ResourceCT.query.filter_by(Path=i).first()
        #     if q is not None:
        #         continue
        #     i = i.strip()  ## whitespace
        #     if i == "" and len(i) > 250:
        #         continue
        #
        #     tmp = dict(Path=i)
        #     result.append(tmp)
        # ### Insert list of dict to database
        # if len(result) == 0:
        #     print("[m] No one.")
        #     exit()
        default = int(os.environ.get('CHUNK_SIZE'))
        size = math.ceil(len(result) / default)
        chunker = numpy.array_split(result, size)
        ### Insert list of dict to database
        for i, v in enumerate(chunker):
            print("[m] Step %d \n[m] Total %d resource relate inserted" % (i, len(v)))
            if cat == 'ttc':
                db.session.bulk_insert_mappings(ResourceRelateC, v)
            else:
                db.session.bulk_insert_mappings(ResourceRelateCT, v)
        db.session.commit()
        print("[m] Inserted resource relate done.")
    except Exception as e:
        tb = sys.exc_info()[2]
        print(e.with_traceback(tb))
        db.session.rollback()
        print(" [x] Fail")


@bd.cli.command('cat')
@click.argument('type')
def buildCats(type):
    try:
        api_url = os.environ.get('MAIN_API') + '/sharecate'
        myobj = {
            "seckey": os.environ.get('seckey'),
            "catid": type,
        }
        response = requests.post(api_url, data=myobj)
        json_response = json.loads(response.text)
        valueList = []

        # Append list objects to new dict collection
        for idx, val in enumerate(json_response):
            tmp = dict(PartnerId=val['Id'], Invisibled=val['Invisibled'], Description="", ShortUrl=val['ShortURL'],
                       SortOrder=val['SortOrder'], ParentShortUrl=val['ParentShortUrl'], Status=val['Status'],
                       Name=val['Name'],
                       ModifiedDate=val['ModifiedDate'], ParentId=val['ParentId'], Mode=val['Mode'],
                       CreatedDate=val['CreatedDate'],
                       AllowComment=val['AllowComment'], ParentName=val['ParentName'], Domain=val['Domain'])
            if type == 'ttc':
                q = TermC.query.filter_by(PartnerId=val['Id']).first()
            else:
                q = TermCT.query.filter_by(PartnerId=val['Id']).first()
            if q is not None:
                continue
            valueList.append(tmp)
            # break
        print(valueList)
        if type == 'ttc':
            db.session.bulk_insert_mappings(TermC, valueList)
        else:
            db.session.bulk_insert_mappings(TermCT, valueList)
        db.session.commit()
        print("Insert cat list done!")
    except Exception as e:
        print(e)
        db.session.rollback()
        print(" [x] Fail")


@bd.cli.command('topic')
@click.argument('type')
def buildTopics(type):
    try:
        api_url = os.environ.get('MAIN_API') + '/sharelisttopic'
        myobj = {
            "seckey": os.environ.get('seckey'),
            "catid": type,
        }
        response = requests.post(api_url, data=myobj)
        json_response = json.loads(response.text)
        valueList = []
        # Append list objects to new dict collection
        for idx, val in enumerate(json_response):
            tmp = dict(PartnerId=val['Id'], Cover=val['Cover'], DefaultViewMode=val['DefaultViewMode'],
                       Description=val['Description'],
                       DisplayUrl=val['DisplayUrl'], GuideToSendMail=val['GuideToSendMail'], IsActive=val['IsActive'],
                       IsIconActive=val['IsIconActive'],
                       Logo=val['Logo'], LogoFancyClose=val['LogoFancyClose'], LogoSubMenu=val['LogoSubMenu'],
                       LogoTopicName=val['LogoTopicName'],
                       TopicEmail=val['TopicEmail'], TopicName=val['TopicName'], isTopToolbar=val['isTopToolbar'],
                       rownum=val['rownum'])
            if type == 'ttc':
                q = TopicC.query.filter_by(PartnerId=val['Id']).first()
            else:
                q = TopicCT.query.filter_by(PartnerId=val['Id']).first()
            if q is not None:
                continue
            valueList.append(tmp)
            # break
        # print(valueList)
        if type == 'ttc':
            db.session.bulk_insert_mappings(TopicC, valueList)
        else:
            db.session.bulk_insert_mappings(TopicCT, valueList)
        db.session.commit()
        print("Insert topic list done!")
    except Exception as e:
        print(e)
        db.session.rollback()
        print(" [x] Fail")


@bd.cli.command('topic-relate')
@click.argument('cat')
@click.argument('size')
@click.argument('fr')
@click.argument('to')
def buildTopicRelate(cat, size, fr, to, ):
    try:
        range = getFrToPam(fr, to)
        json_response = getLst(cat, size, range['fr'], range['to'])
        listTop = valueList = []
        if cat == 'ttc':
            listTop = TopicC.query.all()
        else:
            listTop = TopicCT.query.all()
        newListTop = dict()
        valueList = []
        for i, v in enumerate(listTop):
            newListTop.update({v.PartnerId: v.DisplayUrl})
        for idx, val in enumerate(json_response):
            #################### Topic Handler #####################
            if val['AllTopic'] is not None:
                parse = val['AllTopic']
                if parse:
                    for i, v in enumerate(parse):
                        tmp = dict(ArticleId=val['NewsId'], DisplayUrl=newListTop[v], PartnerId=v)
                        valueList.append(tmp)
            ### Handler exist records ###
            if cat == 'ttc':
                q = TopicRelateC.query.filter_by(ArticleId=val['NewsId']).all()
            else:
                q = TopicRelateCT.query.filter_by(ArticleId=val['NewsId']).all()
            # Delete old relationship by article id
            if q:
                for qi, qv in enumerate(q):
                    db.session.delete(q[qi])
                db.session.commit()
            ##############################
        ### Calculate size of results ###
        if len(valueList) == 0:
            print("[m] No one data.")
            exit()
        default = int(os.environ.get('CHUNK_SIZE'))
        size = math.ceil(len(valueList) / default)
        chunker = numpy.array_split(valueList, size)
        # print(chunker)
        ### Insert list of dict to database
        for i, v in enumerate(chunker):
            print("[m] Step %d \n[m]Total %d\n" % (i, len(v)))
            if type == 'ttc':
                db.session.bulk_insert_mappings(TopicRelateC, v)
            else:
                db.session.bulk_insert_mappings(TopicRelateCT, v)
        db.session.commit()
        ####################################
        print("[m] Inserted topic done.")
    except Exception as e:
        print(e)


@bd.cli.command('thread')
@click.argument('type')
def buildThreads(type):
    try:
        api_url = os.environ.get('MAIN_API') + '/sharelistthread'
        myobj = {
            "seckey": os.environ.get('seckey'),
            "catid": type,
        }
        response = requests.post(api_url, data=myobj)
        json_response = json.loads(response.text)
        valueList = []
        # Append list objects to new dict collection
        for idx, val in enumerate(json_response):
            IsPrimary = val.get('IsPrimary', 0)
            Ordinary = val.get('Ordinary', 0)
            RelationThread = val.get('RelationThread', "")
            RelationZone = val.get('RelationZone', "")
            tmp = dict(PartnerId=val['Id'], ArrZoneId=json.dumps(val['ArrZoneId']), Avatar=val['Avatar'],
                       CreatedBy=val['CreatedBy'],
                       CreatedDate=val['CreatedDate'], Description=val['Description'], EditedBy=val['EditedBy'],
                       ExtensionType=json.dumps(val['ExtensionType']), ExtensionValue=json.dumps(val['ExtensionValue']),
                       HomeAvatar=val['HomeAvatar'],
                       Invisibled=val['Invisibled'], IsHot=val['IsHot'], IsOnHome=val['IsOnHome'], IsPrimary=IsPrimary,
                       MetaContent=val['MetaContent'], MetaKeyword=val['MetaKeyword'], ModifiedDate=val['ModifiedDate'],
                       Name=val['Name'],
                       NewsCoverId=val['NewsCoverId'], Ordinary=Ordinary, RelationThread=RelationThread,
                       RelationZone=RelationZone,
                       SpecialAvatar=val['SpecialAvatar'], TemplateId=val['TemplateId'], Title=val['Title'],
                       Type=val['Type'],
                       UnsignName=val['UnsignName'], Url=val['Url'], ZoneId=val['ZoneId'])
            if type == 'ttc':
                q = ThreadC.query.filter_by(PartnerId=val['Id']).first()
            else:
                q = ThreadCT.query.filter_by(PartnerId=val['Id']).first()
            if q is not None:
                continue
            valueList.append(tmp)
            # if idx == 9:
            #     break
        # print(valueList)
        if type == 'ttc':
            db.session.bulk_insert_mappings(ThreadC, valueList)
        else:
            db.session.bulk_insert_mappings(ThreadCT, valueList)
        db.session.commit()
        print("Insert thread list done!")
    except Exception as e:
        # tb = sys.exc_info()[2]
        # raise e.with_traceback(tb)
        print(e)
        db.session.rollback()
        print(" [x] Fail")


@bd.cli.command('thread-relate')
@click.argument('cat')
@click.argument('size')
@click.argument('fr')
@click.argument('to')
def buildThreadRelate(cat, size, fr, to, ):
    try:
        range = getFrToPam(fr, to)
        json_response = getLst(cat, size, range['fr'], range['to'])
        listTop = valueList = []
        if cat == 'ttc':
            listTop = ThreadC.query.all()
        else:
            listTop = ThreadCT.query.all()
        newListTop = dict()
        valueList = []
        for i, v in enumerate(listTop):
            newListTop.update({v.PartnerId: v.Url})
        # print(newListTop)
        for idx, val in enumerate(json_response):

            #################### Thread Handler #####################
            if len(val['AllThread']) > 0:
                parse = val['AllThread']
                for i, v in enumerate(parse):
                    if v in newListTop:
                        tmp = dict(ArticleId=val['NewsId'], Url=newListTop[v], PartnerId=v)
                        valueList.append(tmp)
            ### Handler exist records ###
            if cat == 'ttc':
                q = ThreadRelateC.query.filter_by(ArticleId=val['NewsId']).all()
            else:
                q = ThreadRelateCT.query.filter_by(ArticleId=val['NewsId']).all()
            # Delete old relationship by article id
            if q:
                for qi, qv in enumerate(q):
                    db.session.delete(q[qi])
                db.session.commit()
            ##############################
        ### Calculate size of results ###
        if len(valueList) == 0:
            print("[m] No one data.")
            exit()
        default = int(os.environ.get('CHUNK_SIZE'))
        size = math.ceil(len(valueList) / default)
        chunker = numpy.array_split(valueList, size)
        ### Insert list of dict to database
        for i, v in enumerate(chunker):
            print("[m] Step %d \n[m]Total %d\n" % (i, len(v)))
            if type == 'ttc':
                db.session.bulk_insert_mappings(ThreadRelateC, v)
            else:
                db.session.bulk_insert_mappings(ThreadRelateCT, v)
        db.session.commit()
        ####################################
        print("[m] Inserted thread done.")
    except Exception as e:
        tb = sys.exc_info()[2]
        print(e.with_traceback(tb))
        db.session.rollback()
        print(" [x] Fail")


@bd.cli.command('author')
@click.argument('cat')
@click.argument('size')
@click.argument('fr')
@click.argument('to')
def buildAuthors(cat, size, fr, to):
    try:
        range = getFrToPam(fr, to)
        json_response = getLst(cat, size, range['fr'], range['to'])
        valueList = []
        # Append list objects to new dict collection
        for idx, val in enumerate(json_response):
            if "AuthorName" not in val:
                authorName = val['Author']
            else:
                authorName = val['AuthorName']
            tmp = dict(PartnerId=val['AuthorId'], AuthorDisplayName=val['Author'], AuthorName=authorName,
                       AuthorUrl=val['AuthorUrl'])
            if cat == 'ttc':
                q = AuthorC.query.filter_by(PartnerId=val['AuthorId'], AuthorUrl=val['AuthorUrl']).first()
            else:
                q = AuthorCT.query.filter_by(PartnerId=val['AuthorId'], AuthorUrl=val['AuthorUrl']).first()
            if q is not None:
                continue
            valueList.append(tmp)
            # break
        valueList = unique(valueList)
        if cat == 'ttc':
            db.session.bulk_insert_mappings(AuthorC, valueList)
        else:
            db.session.bulk_insert_mappings(AuthorCT, valueList)
        print("[m]Total %d\n" % len(valueList))
        db.session.commit()
        print("Insert author list done!")
    except Exception as e:
        print(e)
        db.session.rollback()
        print(" [x] Fail")


@bd.cli.command('author-relate')
@click.argument('cat')
@click.argument('size')
@click.argument('fr')
@click.argument('to')
def buildAuthorRelate(cat, size, fr, to):
    try:
        range = getFrToPam(fr, to)
        json_response = getLst(cat, size, range['fr'], range['to'])
        listTop = valueList = []
        if cat == 'ttc':
            listTop = AuthorC.query.all()
        else:
            listTop = AuthorCT.query.all()
        newListTop = dict()
        valueList = []
        for idx, val in enumerate(json_response):
            #################### Author Handler #####################
            if "AuthorName" not in val:
                authorName = val['Author']
            else:
                authorName = val['AuthorName']
            tmp = dict(ArticleId=val['NewsId'], AuthorUrl=val['AuthorUrl'], AuthorName=authorName)
            valueList.append(tmp)
            ### Handler exist records ###
            if cat == 'ttc':
                q = AuthorRelateC.query.filter_by(ArticleId=val['NewsId']).all()
            else:
                q = AuthorRelateCT.query.filter_by(ArticleId=val['NewsId']).all()
            # Delete old relationship by article id
            if q:
                for qi, qv in enumerate(q):
                    db.session.delete(q[qi])
                db.session.commit()
            ##############################
        ### Calculate size of results ###
        valueList = unique(valueList)
        if len(valueList) == 0:
            print("[m] No one data.")
            exit()
        default = int(os.environ.get('CHUNK_SIZE'))
        size = math.ceil(len(valueList) / default)
        chunker = numpy.array_split(valueList, size)
        ### Insert list of dict to database
        for i, v in enumerate(chunker):
            print("[m] Step %d \n[m]Total %d\n" % (i, len(v)))
            if cat == 'ttc':
                db.session.bulk_insert_mappings(AuthorRelateC, v)
            else:
                db.session.bulk_insert_mappings(AuthorRelateCT, v)
        db.session.commit()
        ####################################
        print("[m] Inserted thread done.")
    except Exception as e:
        tb = sys.exc_info()[2]
        print(e.with_traceback(tb))
        db.session.rollback()
        print(" [x] Fail")


@bd.cli.command('object')
@click.argument('cat')
@click.argument('size')
@click.argument('fr')
@click.argument('to')
def buildObject(cat, size, fr, to):
    try:
        range = getFrToPam(fr, to)
        json_response = getLst(cat, size, range['fr'], range['to'])
        valueList = []
        # Append list objects to new dict collection
        for idx, val in enumerate(json_response):
            LastModifiedDateTimestamp = toTimestamp(val['LastModifiedDate'])
            Extension = val.get('Extension', [])
            SocialTitle = val.get('SocialTitle', "")
            MetaTitle = val.get('MetaTitle', "")
            MetaNewsKeyword = val.get('MetaNewsKeyword', "")
            MetaKeyword = val.get('MetaKeyword', "")
            MetaDescription = val.get('MetaDescription', "")
            KeywordFocus = val.get('KeywordFocus', "")
            AllVideo = val.get('AllVideo', [])
            tmp = dict(isOld=val['isOld'], ZoneId=val['ZoneId'], WordCount=val['WordCount'], Url=val['Url'],
                       Type=val['Type'], Title=val['Title'], ThreadId=val['ThreadId'], TagSubTitleId=val['TagSubTitleId'],
                       TagPrimary=val['TagPrimary'], TagItem=val['TagItem'], Tag=json.dumps(val['Tag']), SubTitle=val['SubTitle'],
                       SourceUrl=val['SourceUrl'], Source=val['Source'], SocialTitle=SocialTitle, Sapo=val['Sapo'],
                       RollingNewsId=val['RollingNewsId'], PrPosition=val['PrPosition'], Position=val['Position'],
                       ParentNewsId=val['ParentNewsId'], OriginalUrl=val['OriginalUrl'], OriginalId=val['OriginalId'],
                       NewsType=val['NewsType'], NewsRelation=val['NewsRelation'], MetaTitle=MetaTitle,
                       MetaNewsKeyword=MetaNewsKeyword, MetaKeyword=MetaKeyword, MetaDescription=MetaDescription,
                       LocationType=val['LocationType'], LastModifiedDate=val['LastModifiedDate'], KeywordFocus=KeywordFocus,
                       IsOnHome=val['IsOnHome'], InterviewId=val['InterviewId'], InitSapo=val['InitSapo'],
                       ExtentionValue=json.dumps(val['ExtentionValue']), ExtentionType=json.dumps(val['ExtentionType']),
                       Extention=json.dumps(Extension), ExpiredDate=val['ExpiredDate'], DistributionDate=val['DistributionDate'],
                       DisplayInSlide=val['DisplayInSlide'], Body=val['Body'], AvatarDesc=val['AvatarDesc'],
                       Avatar5=val['Avatar5'], Avatar4=val['Avatar4'], Avatar3=val['Avatar3'], Avatar2=val['Avatar2'],
                       Avatar=val['Avatar'], AuthorUrl=val['AuthorUrl'], AuthorId=val['AuthorId'], Author=val['Author'],
                       AllZone=json.dumps(val['AllZone']), AllTopic=json.dumps(val['AllTopic']), AllThread=json.dumps(val['AllThread']),
                       AdStoreUrl=val['AdStoreUrl'], AdStore=val['AdStore'], PartnerId=val['NewsId'], AllVideo=json.dumps(AllVideo),
                       LastModifiedDateTimestamp=LastModifiedDateTimestamp)
            if cat == 'ttc':
                q = ObjectCT.query.filter_by(PartnerId=val['NewsId']).first()
            else:
                q = ObjectCT.query.filter_by(PartnerId=val['NewsId']).first()
            if q is not None:
                continue
            valueList.append(tmp)
        ### Calculate size of results ###
        valueList = unique(valueList)
        if len(valueList) == 0:
            print("[m] No one data.")
            exit()
        default = int(os.environ.get('CHUNK_SIZE'))
        size = math.ceil(len(valueList) / default)
        chunker = numpy.array_split(valueList, size)
        ### Insert list of dict to database
        for i, v in enumerate(chunker):
            print("[m] Step %d \n[m]Total %d\n" % (i, len(v)))
            if cat == 'ttc':
                db.session.bulk_insert_mappings(ObjectC, v)
            else:
                db.session.bulk_insert_mappings(ObjectCT, v)
        db.session.commit()
        print("Insert object list done!")
    except Exception as e:
        db.session.rollback()
        print(" [x] Fail")
        tb = sys.exc_info()[2]
        raise e.with_traceback(tb)