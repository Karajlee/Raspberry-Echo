import sys
import paho.mqtt.client as mqtt
import time
# use grovepi and lcd display
import grovepi
from grove_rgb_lcd import *
# we are successfully `import grovepi`
sys.path.append('../../Software/Python/')
# This append is to support importing the LCD library.
sys.path.append('../../Software/Python/grove_rgb_lcd')

# port D2
led = 2


def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to topics of interest here - lcd,led
    client.subscribe("christellekara/light")
    client.message_callback_add("christellekara/light",light)
    client.subscribe("christellekara/lcd")
    client.message_callback_add("christellekara/lcd", lcd_out)
    client.subscribe("christellekara/red")
    client.message_callback_add("christellekara/red", on_red)
    client.subscribe("christellekara/orange")
    client.message_callback_add("christellekara/orange", on_orange)
    client.subscribe("christellekara/white")
    client.message_callback_add("christellekara/white", on_white)
    client.subscribe("christellekara/yellow")
    client.message_callback_add("christellekara/yellow", on_yellow)
    client.subscribe("christellekara/green")
    client.message_callback_add("christellekara/green", on_green)
    client.subscribe("christellekara/blue")
    client.message_callback_add("christellekara/blue", on_blue)
    client.subscribe("christellekara/purple")
    client.message_callback_add("christellekara/purple", on_purple)

def light(client, userdata, msg):
    # 'turn off light' turns off led and 'turn on light' turns on led
    if str(msg.payload, "utf-8") == "off":
        grovepi.digitalWrite(led,0)
    elif str(msg.payload, "utf-8") == "on":
        grovepi.digitalWrite(led,1)
    

def on_red(client, userdata, msg):
    setRGB(200,0,0)

def on_orange(client, userdata, msg):
    setRGB(210, 90, 0)

def on_white(client, userdata, msg):
    setRGB(150, 87, 51)
    
def on_yellow(client, userdata, msg):
    setRGB(150, 90, 0)

def on_green(client, userdata, msg):
    setRGB(0, 255, 0)

def on_blue(client, userdata, msg):
    setRGB(0, 0, 255)
    
def on_purple(client, userdata, msg):
    setRGB(138,43,226)
    
    
#Default message callback
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))
    
def lcd_out(client, userdata, msg):
    # takes in msg and prints it out 
    text = str(msg.payload, "utf-8")
    setText_norefresh(text)
    

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()
    # turn on backlight 
    setRGB(0,0,255)
    while True: 
        time.sleep(1)