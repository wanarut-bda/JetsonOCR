import paho.mqtt.client as mqtt
import random as rd
import time

host = "192.168.88.61"
port = 1885

client = mqtt.Client()
client.connect(host, port)
for i in range(60):
    client.publish("heart_rate/1", rd.randint(60, 150))
    print("mqtt sent")
    time.sleep(1)