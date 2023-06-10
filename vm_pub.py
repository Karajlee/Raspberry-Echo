import paho.mqtt.client as mqtt
import time
from pynput import keyboard
import pyaudio
import websockets
import asyncio
import base64
import json



def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))


#Default message callback
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

def on_press(key):
    auth_key = '787cdfa24a6645489dfc1579517d83bb'

    FRAMES_PER_BUFFER = 3200
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    p = pyaudio.PyAudio()

    # starts recording
    stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=FRAMES_PER_BUFFER
    )

    # the AssemblyAI endpoint we're going to hit
    URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"

    async def send_receive():
        print(f'Connecting websocket to url ${URL}')
        async with websockets.connect(
            URL,
            extra_headers=(("Authorization", auth_key),),
            ping_interval=5,
            ping_timeout=20
        ) as _ws:
            await asyncio.sleep(0.1)
            print("Receiving SessionBegins ...")
            session_begins = await _ws.recv()
            print(session_begins)
            print("Sending messages ...")
            async def send():
                while True:
                    try:
                        data = stream.read(FRAMES_PER_BUFFER)
                        data = base64.b64encode(data).decode("utf-8")
                        json_data = json.dumps({"audio_data":str(data)})
                        await _ws.send(json_data)
                    except websockets.exceptions.ConnectionClosedError as e:
                        print(e)
                        assert e.code == 4008
                        break
                    except Exception as e:
                        assert False, "Not a websocket 4008 error"
                    await asyncio.sleep(0.01)

                return True

            async def receive():
                while True:
                    try:
                        result_str = await _ws.recv()
                        publish_text = json.loads(result_str)['text']
                        print(publish_text)
                        client.publish("christellekara/lcd",publish_text)
                        if "red" in publish_text.lower():
                            client.publish("christellekara/red",publish_text)
                        if "orange" in publish_text.lower():
                            client.publish("christellekara/orange",publish_text)
                        if "yellow" in publish_text.lower():
                            client.publish("christellekara/yellow",publish_text)
                        if "green" in publish_text.lower():
                            client.publish("christellekara/green",publish_text)
                        if "blue" in publish_text.lower():
                            client.publish("christellekara/blue",publish_text)
                        if "purple" in publish_text.lower():
                            client.publish("christellekara/purple",publish_text)
                        if "white" in publish_text.lower():
                            client.publish("christellekara/white",publish_text)
                        if ("turn light on" in publish_text.lower()) or ("turn on light" in publish_text.lower()) or ("turn on led" in publish_text.lower()) or ("turn led on" in publish_text.lower()):
                            client.publish("christellekara/light","on")
                        if ("turn light off" in publish_text.lower()) or ("turn off light" in publish_text.lower()) or ("turn off led" in publish_text.lower()) or ("turn led off" in publish_text.lower()):
                            client.publish("christellekara/light","off")
                    except websockets.exceptions.ConnectionClosedError as e:
                        print(e)
                        assert e.code == 4008
                        break
                    except Exception as e:
                        assert False, "Not a websocket 4008 error"

            send_result, receive_result = await asyncio.gather(send(), receive())


    asyncio.run(send_receive())


if __name__ == '__main__':
    #setup the keyboard event listener
    lis = keyboard.Listener(on_press=on_press)
    lis.start() # start to listen on a separate thread

    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()
    while True:
        time.sleep(1)