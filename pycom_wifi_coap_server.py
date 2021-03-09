from network import WLAN
import machine
from microcoapy.microcoapy import Coap
from microcoapy.coap_macros import COAP_CONTENT_FORMAT
from microcoapy.coap_macros import COAP_RESPONSE_CODE
from microcoapy.coap_macros import COAP_METHOD

import microcoapy.microcoapy as microcoapy
import utime as time
import pycom

wlan = WLAN(mode=WLAN.STA)

_MY_SSID = 'ssid'
_MY_PASS = 'passwd'
_SERVER_PORT = 5683  # default CoAP port


def connectToWiFi():
    print('Starting attempt to connect to WiFi...')
    nets = wlan.scan()
    for net in nets:
        if net.ssid == _MY_SSID:
            print('Network found!')
            wlan.connect(net.ssid, auth=(net.sec, _MY_PASS), timeout=5000)
            while not wlan.isconnected():
                machine.idle()  # save power while waiting

            connectionResults = wlan.ifconfig()
            print('WLAN connection succeeded with IP: ', connectionResults[0])
            break

    return wlan.isconnected()

connectToWiFi()
#stop the blinking led
pycom.heartbeat(False)
global color
color = 0x000000 

def RGBLed(packet, senderIp, senderPort):
    global color
    #check if it iis GET or PUT, we can reject others for the moment
    if packet.method == COAP_METHOD.COAP_GET:

        print('GET RGB Led request received:', packet, ', from: ', senderIp, ":", senderPort)
        
        client.sendResponse(senderIp, senderPort, packet.messageid,
                      str(color), microcoapy.COAP_RESPONSE_CODE.COAP_CONTENT,
                      microcoapy.COAP_CONTENT_FORMAT.COAP_NONE, packet.token)
    elif packet.method == COAP_METHOD.COAP_PUT:
        if packet.payload :
            color = int(packet.payload)
            print('Changing color to', color)
            pycom.rgbled(color)
            client.sendResponse(senderIp, senderPort, packet.messageid,
                      str(color), microcoapy.COAP_RESPONSE_CODE.COAP_CHANGED,
                      microcoapy.COAP_CONTENT_FORMAT.COAP_NONE, packet.token)
        else:
            client.sendResponse(senderIp, senderPort, packet.messageid,
                      "", microcoapy.COAP_RESPONSE_CODE.COAP_BAD_REQUEST,
                      microcoapy.COAP_CONTENT_FORMAT.COAP_NONE, packet.token)

    else:
        client.sendResponse(senderIp, senderPort, packet.messageid,
                      "", microcoapy.COAP_RESPONSE_CODE.COAP_METHOD_NOT_ALLOWD,
                      microcoapy.COAP_CONTENT_FORMAT.COAP_NONE, packet.token)
  
 

def temperature(packet, senderIp, senderPort):
    print('Turn-off-led request received:', packet, ', from: ', senderIp, ":", senderPort)
    client.sendResponse(senderIp, senderPort, packet.messageid,
                      "ok", microcoapy.COAP_RESPONSE_CODE.COAP_CONTENT,
                      microcoapy.COAP_CONTENT_FORMAT.COAP_NONE, packet.token)
    pycom.rgbled(0)


client = microcoapy.Coap()
# setup callback for incoming response to a request
client.addIncomingRequestCallback('pycom/rgbled', RGBLed)
client.addIncomingRequestCallback('pysense/temperature', temperature)

# Starting CoAP...
client.start()

# wait for incoming request for 600 seconds
timeoutMs = 600000
start_time = time.ticks_ms()
while time.ticks_diff(time.ticks_ms(), start_time) < timeoutMs:
    client.poll(60000)

# stop CoAP
client.stop()
