# from flask import Blueprint, jsonify, request
# import click
import json
import os
import webbrowser
import requests
from flask import Blueprint, jsonify

api = Blueprint('endpoint', __name__)


@api.route("/runner", methods=['GET'])
def runner():
    try:
        return jsonify(
            status=200,
            message="Delete success!",
        )
    except Exception as e:
        print(e)

