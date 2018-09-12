import json
import random

from flask import Flask, request
app = Flask(__name__)

from generate import PostalGenerator

@app.route('/')
def hello_world():
    return 'Hello, World!'

def randTime(size=100):
    timings = [700, 730, 800, 830, 900]
    return (random.choices(timings, k=size))


@app.route('/generate', methods=['POST'])
def run_generation():
    pg = PostalGenerator('./postal_code_to_address.csv')
    req = request.get_json()
    size = req['size']
    resp = pg.receive(req['origins'], req['destinations'], .15, 300, size)

    randomTimes = randTime()
    rows = []
    rows.append("Index,Origin,Destination,Time")
    for i in range(size):
        rows.append("{},{},{},{}".format(i, resp['o'][i], resp['d'][i], randomTimes[i]))

    return json.dumps({'resp': rows})
