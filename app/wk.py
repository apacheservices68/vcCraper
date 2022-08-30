import os
import re
import sys
import requests
import click
from flask import Blueprint, jsonify, request
import pika
import logging
import time
from os import environ

worker = Blueprint("command", __name__, url_prefix='/command')
logging.basicConfig()
wk = Blueprint('queue', __name__)


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())
    try:
        results = body.decode().split(',', -1)
        tmp = dict(Domain=results[0], Path=results[1], Filename=results[2])
        # Download workflow here
        saveTo(tmp, results[3])
        print(" [x] Done")
        # time.sleep(body.count(b'.'))
    except Exception as e:
        print(" [x] Fail")
        tb = sys.exc_info()[2]
        raise e.with_traceback(tb)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def saveTo(infos, cat):
    url = infos['Domain'] + infos['Path'] + infos['Filename']
    # print(url)
    y = re.search("^.*mp3$", infos['Filename'])
    if y:
        x = re.search("^\/?tto\/r.*$", infos['Path'])
        if x:
            infos['Path'] = "/tto/r" + infos['Path']
    url = infos['Domain'] + infos['Path'] + infos['Filename']
    path = re.sub(r"\/\/", r"/", os.environ.get("RESOURCE_PATH") + cat + infos['Path'])
    filePath = path + infos['Filename']
    if os.path.exists(filePath):
        print(" [m] File exist ", filePath)
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


@wk.cli.command("worker")
@click.argument('path')
def run(path):
    url = os.environ.get('CLOUDAMQP_URL')
    queueName = "download_queue"
    parameters = pika.URLParameters(url)
    parameters.socket_timeout = 5
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue=queueName, durable=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queueName, on_message_callback=callback)

    channel.start_consuming()
