# pycom-coap
Pycom coap server and client
This is an example implementation of CoAP server and client using the library [microCoAPy](https://github.com/insighio/microCoAPy)

The CoAP server allows the coap clients to change the color of the RGB LED (imagine it to be your IoT lamp) from remote.

Tested with libcoap coap-client. Run pycom_wifi_coap_server.py on a Pycom and obtain its IP address. Here we assume it to be 192.168.0.35. Then install libcoap and coap-client on your PC. After that you can interact with the Pycom from your PC using following commands.  

To GET the current color:

coap-client -m get coap://192.168.0.35/pycom/rgbled

To PUT a value of color:

echo -n "0x00000f" | coap-client -m put coap://192.168.0.35/pycom/rgbled -f-
