# pycom-coap
pycom coap server and client
This is an example implementation of CoAP server and client using the library [microCoAPy](https://github.com/insighio/microCoAPy)

The CoAP server allows the coap clients to change the color of the RGB LED.

Tested with libcoap coap-client.
To GET the current color:
coap-client -m get coap://192.168.0.35/pycom/rgbled

To PUT a value of color:
echo -n "0x00000f" | coap-client -m put coap://192.168.0.35/pycom/rgbled -f-
