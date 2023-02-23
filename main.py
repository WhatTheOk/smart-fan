def on_button_pressed_a():
    fanData[1] = (int(fanData[1] / 3) * 3) % 9 + 3
input.on_button_pressed(Button.A, on_button_pressed_a)

def on_button_pressed_b():
    fanData[0] = (fanData[0] + 1) % 4
    pins.digital_write_pin(DigitalPin.P8, 0)
    pins.digital_write_pin(DigitalPin.P9, 0)
    pins.digital_write_pin(DigitalPin.P10, 0)
    if fanData[0] == 1:
        pins.digital_write_pin(DigitalPin.P9, 1)
    elif fanData[0] == 2:
        pins.digital_write_pin(DigitalPin.P10, 1)
        ds.set_second(0)
        ds.set_minute(0)
        ds.set_hour(0)
    elif fanData[0] == 3:
        pins.digital_write_pin(DigitalPin.P8, 1)
input.on_button_pressed(Button.B, on_button_pressed_b)

def on_forever():
    if fanData[0] == 3:
        pass
    elif fanData[0] == 2:
        pass
    elif fanData[0] == 1:
        fanSpeed(fanData[1])
    elif fanData[0] == 0:
        fanSpeed(0)
    basic.pause(2000)

basic.forever(on_forever)

def fanSpeed(speed):
    pins.analog_write_pin(AnalogPin.P4, 348 + speed * 75)
    if speed == 0:
        pins.analog_write_pin(AnalogPin.P4, 0)

led.enable(False)
fanData = [0, 5, 2, 30, 20, 30]
makerbit.connect_ir_receiver(DigitalPin.P0, IrProtocol.KEYESTUDIO)
ds = DS1302.create(DigitalPin.P13, DigitalPin.P14, DigitalPin.P15)
dht11_dht22.query_data(DHTtype.DHT11, DigitalPin.P1, True, False, False)
