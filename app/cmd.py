# from flask import Blueprint, jsonify, request
# import click
import json
import os
import webbrowser
import requests
from flask import Blueprint

bd = Blueprint('import', __name__)
api_url = os.environ.get('MAIN_API') + '/sharelistnewstopic'


@bd.cli.command('list')
def buildData():
    try:
        myobj = {
            "seckey": os.environ.get('seckey'),
            "topicid": 603,
            "page": 0,
            "size": 1
        }
        response = requests.post(api_url, data=myobj)
        json_response = json.loads(response.text)
        photo_url = os.environ.get('MAIN_DOMAIN') + json_response[0]['Url']
        webbrowser.open_new_tab(photo_url)
        print("DEMO done!")
    except Exception as e:
        print(e)
