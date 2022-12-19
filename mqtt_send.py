from dotenv import load_dotenv
import os
import paho.mqtt.publish as publish
load_dotenv()

payload ={''}
auth = {'username': "timothy", 'password': os.environ['MQTT_PASS']}
def send(data,topic='Machine'):
    data=str(data)
    publish.single('RoadParking/'+topic, data, qos=2, hostname='mqtt.ckcsc.net',port=5900,auth=auth)
