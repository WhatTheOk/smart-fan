def on_button_pressed_a():
    fanData[1] = (int(fanData[1] / 3) * 3) % 9 + 3
input.on_button_pressed(Button.A, on_button_pressed_a)

def on_button_pressed_b():
    changeMode((fanData[0] + 1) % 5)
input.on_button_pressed(Button.B, on_button_pressed_b)

def on_received_string(data):
    fanData[1] = int(data[1])
    for i in range(2,6):
        fanData[i] = int(data[i * 2 - 2:i * 2])
    changeMode(int(data[0]))
radio.on_received_string(on_received_string)

def on_ir_button_any_pressed():
    if changeData == -1:
        if makerbit.ir_button() == makerbit.ir_button_code(IrButton.NUMBER_1):
            changeMode(0)
        elif makerbit.ir_button() == makerbit.ir_button_code(IrButton.NUMBER_2):
            changeMode(1)
        elif makerbit.ir_button() == makerbit.ir_button_code(IrButton.NUMBER_3):
            changeMode(2)
        elif makerbit.ir_button() == makerbit.ir_button_code(IrButton.NUMBER_4):
            changeMode(3)
        elif makerbit.ir_button() == makerbit.ir_button_code(IrButton.NUMBER_5):
            changeMode(4)
        elif makerbit.ir_button() == makerbit.ir_button_code(IrButton.STAR):
            irChangeData(0)
        elif makerbit.ir_button() == makerbit.ir_button_code(IrButton.NUMBER_0):
            irChangeData(1)
        elif makerbit.ir_button() == makerbit.ir_button_code(IrButton.HASH):
            irChangeData(2)
makerbit.on_ir_button(IrButton.ANY, IrButtonAction.PRESSED, on_ir_button_any_pressed)

def irChangeData(data):
    global changeData
    changeData = data
    if changeData == 1:
        for i in range(30):
            if makerbit.was_ir_data_received():
                if makerbit.ir_button() > 0:
                    fanSpeed(makerbit.ir_button())
                break
            basic.pause(100)
    changeData = -1

def changeMode(mode):
    fanData[0] = mode
    pins.digital_write_pin(DigitalPin.P8, 0)
    pins.digital_write_pin(DigitalPin.P9, 0)
    pins.digital_write_pin(DigitalPin.P10, 0)
    if fanData[0] == 1:
        pins.digital_write_pin(DigitalPin.P9, 1)
    if fanData[0] == 2 or fanData[0] == 4:
        pins.digital_write_pin(DigitalPin.P10, 1)
        ds.set_second(0)
        ds.set_minute(0)
        ds.set_hour(0)
    if fanData[0] == 3 or fanData[0] == 4:
        pins.digital_write_pin(DigitalPin.P8, 1)

def on_forever():
    if fanData[0] == 0:
            fanSpeed(0)
    elif fanData[0] == 1:
        fanSpeed(fanData[1])
    elif fanData[0] == 2:
        fanSpeed(fanData[1])
        if fanData[2] == ds.get_hour() and fanData [3] == ds.get_minute():
            changeMode(0)
    elif fanData[0] == 3 or 4:
        temperature = dht11_dht22.read_data(dataType.TEMPERATURE)
        minTemp = fanData[4]
        maxTemp = fanData[5]
        if temperature <= minTemp:
            fanSpeed(0)
        elif temperature >= maxTemp:
            fanSpeed(9)
        else:
            fanSpeed(int((temperature - minTemp) / (maxTemp - minTemp) * 9))
        if fanData[0] == 4:
            if fanData[2] == ds.get_hour() and fanData [3] == ds.get_minute():
                changeMode(0)
    basic.pause(2000)
basic.forever(on_forever)

def fanSpeed(speed):
    pins.analog_write_pin(AnalogPin.P4, 348 + speed * 75)
    if speed == 0:
        pins.analog_write_pin(AnalogPin.P4, 0)

led.enable(False)
fanData = [0, 5, 0, 1, 10, 15]
makerbit.connect_ir_receiver(DigitalPin.P0, IrProtocol.KEYESTUDIO)
ds = DS1302.create(DigitalPin.P13, DigitalPin.P14, DigitalPin.P15)
dht11_dht22.query_data(DHTtype.DHT11, DigitalPin.P1, True, False, False)
changeData = -1
radio.set_group(1)