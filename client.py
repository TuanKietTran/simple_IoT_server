import socketio
import json

# standard Python
sio = socketio.Client()

sio.connect('http://127.0.0.1:5000')
data = {
  "topic": "mytopic",
  "message": '''{
    "device
    "temp": 306.15,
    "pressure": 1013,
    "humidity": 44,
    "temp_min": 306, 
    "temp_max": 306
  }'''
}

re_data = {
  "topic": "mytopic"
}

# sio.emit('publish', json.dumps(data))
# sio.emit('subcribe', json.dumps(re_data))
