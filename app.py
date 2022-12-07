# import eventlet
import json
from flask import Flask, render_template, request, jsonify
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap
from flask_cors import CORS, cross_origin

from pymongo import MongoClient

def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb+srv://user:pass@cluster.mongodb.net/myFirstDatabase"
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client['user_shopping_list']


app = Flask(__name__, template_folder='./templates',
            static_folder='./templates/assets')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# use the free broker from HIVEMQ
app.config['MQTT_BROKER_URL'] = 'broker.hivemq.com'
app.config['MQTT_BROKER_PORT'] = 1883  # default port for non-tls connection
# set the username here if you need authentication for the broker
app.config['MQTT_USERNAME'] = ''
# set the password here if the broker demands authentication
app.config['MQTT_PASSWORD'] = ''
# set the time interval for sending a ping to the broker to 5 seconds
app.config['MQTT_KEEPALIVE'] = 5
# set TLS to disabled for testing purposes
app.config['MQTT_TLS_ENABLED'] = False
topic = 'mytopic'
# Parameters for SSL enabled
# app.config['MQTT_BROKER_PORT'] = 8883
# app.config['MQTT_TLS_ENABLED'] = True
# app.config['MQTT_TLS_INSECURE'] = True
# app.config['MQTT_TLS_CA_CERTS'] = 'ca.crt'
mqtt = Mqtt(app)
socketio = SocketIO(app)
bootstrap = Bootstrap(app)

# client = MongoClient('localhost', 27017)

# db = client.flask_db


@app.route('/')
@cross_origin()
def index():
    return render_template('index.html')


@app.route('/pages/dashboard')
@app.route('/dashboard')
@cross_origin()
def dashboard():
    return render_template('pages/dashboard.html')


@app.route('/pages/tables')
@app.route('/tables')
@cross_origin()
def table():
    return render_template('pages/tables.html')


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Connected successfully')
        mqtt.subscribe(topic)  # subscribe topic
    else:
        print('Bad connection. Code:', rc)


# @socketio.on('publish')
# def handle_publish(json_str):
#     data = json.loads(json_str)
#     mqtt.publish(data['topic'], data['message'])


# @socketio.on('subscribe')
# def handle_subscribe(json_str):
#     data = json.loads(json_str)
#     mqtt.subscribe(data['topic'])


# @socketio.on('unsubscribe_all')
# def handle_unsubscribe_all():
#     mqtt.unsubscribe_all()


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    print(
        'Received message on topic: {topic} with payload: {payload}'.format(**data))


@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)


@app.route('/publish', methods=['POST'])
def publish_message():
    request_data = request.get_json()
    publish_result = mqtt.publish(request_data['topic'], request_data['msg'])
    return jsonify({'code': publish_result[0]})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
