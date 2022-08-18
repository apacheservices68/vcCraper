# from flask import Blueprint, jsonify, request
import click
import json
import os
import re
import webbrowser
import requests
from flask import Blueprint
from app import db
from app.models import TermC, TermCT, TagC, TagCT, TagRelateC, TagRelateCT

bd = Blueprint('import', __name__)


@bd.cli.command('list')
@click.argument('cat')
@click.argument('size')
def buildData(cat, size):
    try:
        api_url = os.environ.get('MAIN_API') + '/sharelistnews'
        myobj = {
            "seckey": os.environ.get('seckey'),
            "catid": cat,
            "size": size,
            "page": 0
            # "order" : "desc"
        }
        response = requests.post(api_url, data=myobj)
        json_response = json.loads(response.text)
        for idx, val in enumerate(json_response):
            parse = json.loads(val['Tag'])
            # print(parse[0])
            print(val['Title'],"\t" , val['AllThread'], "\t", val['AllTopic'])
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
def buildData(type, cat, size):
    try:
        api_url = os.environ.get('MAIN_API') + '/sharelistnews'
        myobj = {
            "seckey": os.environ.get('seckey'),
            "catid": cat,
            "size": size,
            "page": 0
        }
        response = requests.post(api_url, data=myobj)
        json_response = json.loads(response.text)
        tagValueList = []
        for idx, val in enumerate(json_response):
            # print(val['NewsId'], val['Title'])

            #################### Tag Handler #####################
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
        print(result)
        print("\n")

        ### Insert list of dict to database
        if type == 'ttc':
            db.session.bulk_insert_mappings(TagC, result)
        else:
            db.session.bulk_insert_mappings(TagCT, result)
        db.session.commit()
        print("[m] Inserted tag done.")
    except Exception as e:
        print(e)


@bd.cli.command('tag-relate')
@click.argument('type')
@click.argument('cat')
@click.argument('size')
def buildData(type, cat, size):
    try:
        api_url = os.environ.get('MAIN_API') + '/sharelistnews'
        myobj = {
            "seckey": os.environ.get('seckey'),
            "catid": cat,
            "size": size,
            "page": 0
        }
        response = requests.post(api_url, data=myobj)
        json_response = json.loads(response.text)
        tagValueList = []
        for idx, val in enumerate(json_response):
            # print(val['NewsId'], val['Title'])

            #################### Tag Handler #####################
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
        print(result)
        print("\n")
        ## Insert list of dict to database
        if type == 'ttc':
            db.session.bulk_insert_mappings(TagRelateC, result)
        else:
            db.session.bulk_insert_mappings(TagRelateCT, result)
        db.session.commit()
        print("[m] Inserted tag done.")
    except Exception as e:
        print(e)


@bd.cli.command('resources')
@click.argument('type')
@click.argument('cat')
@click.argument('size')
def buildData(type, cat, size):
    try:
        api_url = os.environ.get('MAIN_API') + '/sharelistnews'
        myobj = {
            "seckey": os.environ.get('seckey'),
            "catid": cat,
            "size": size,
            "page": 0
        }
        response = requests.post(api_url, data=myobj)
        json_response = json.loads(response.text)
        valueList = []
        replList = ["//cdn.tuoitre.vn", "tuoitre"]
        for idx, val in enumerate(json_response):
            regex = r"([\/\w+.])+([\/\d+.])+([\w\s_\\.\-\(\):])+(.jpg|.mp4|.jpeg|.gif)"
            matches = re.finditer(regex, val['Body'], re.MULTILINE)
            for matchNum, match in enumerate(matches, start=1):
                tmp = match.group()
                # tmp = re.sub(r"^(.*tuoitre\.vn|tuoitre)", "", tmp)
                tmp = re.sub(r"(.*)(\/\d{4}\/\d{1,2}\/\d{1,2}\/([\w\s_\\.\-\(\):])+(.jpg|.mp4|.jpeg|.gif))", r"\2", tmp)
                valueList.append(tmp)
                # print("Match {match}".format(match=match.group()))
                # for groupNum in range(0, len(match.groups())):
                #     groupNum = groupNum + 1
                #
                #     print("Group {groupNum} found at {start}-{end}: {group}".format(groupNum=groupNum,
                #                                                                     start=match.start(groupNum),
                #                                                                     end=match.end(groupNum),
                #                                                                     group=match.group(groupNum)))
            print("\n")
            # break

        ### Remove duplicate dict from list
        result = []
        for i in valueList:
            if i not in result:
                result.append(i)
        print(result)
        print("\n")
        ## Insert list of dict to database
        # if type == 'ttc':
        #     db.session.bulk_insert_mappings(TagRelateC, result)
        # else:
        #     db.session.bulk_insert_mappings(TagRelateCT, result)
        # db.session.commit()
        print("[m] Inserted tag done.")
    except Exception as e:
        print(e)



@bd.cli.command('cat')
@click.argument('type')
def getCat(type):
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
        print("DEMO done!")
    except Exception as e:
        print(e)
        db.session.rollback()
        print(" [x] Fail")
