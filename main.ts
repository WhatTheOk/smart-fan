input.onButtonPressed(Button.A, function on_button_pressed_a() {
    fanData[1] = Math.trunc(fanData[1] / 3) * 3 % 9 + 3
})
input.onButtonPressed(Button.B, function on_button_pressed_b() {
    changeMode((fanData[0] + 1) % 5)
})
radio.onReceivedString(function on_received_string(data: string) {
    fanData[1] = parseInt(data[1])
    for (let i = 2; i < 6; i++) {
        fanData[i] = parseInt(data.slice(i * 2 - 2, i * 2))
    }
    changeMode(parseInt(data[0]))
})
function changeMode(mode: number) {
    fanData[0] = mode
    pins.digitalWritePin(DigitalPin.P8, 0)
    pins.digitalWritePin(DigitalPin.P9, 0)
    pins.digitalWritePin(DigitalPin.P10, 0)
    if (fanData[0] == 1) {
        pins.digitalWritePin(DigitalPin.P9, 1)
    }
    
    if (fanData[0] == 2 || fanData[0] == 4) {
        pins.digitalWritePin(DigitalPin.P10, 1)
        ds.setSecond(0)
        ds.setMinute(0)
        ds.setHour(0)
    }
    
    if (fanData[0] == 3 || fanData[0] == 4) {
        pins.digitalWritePin(DigitalPin.P8, 1)
    }
    
}

basic.forever(function on_forever() {
    let temperature: number;
    let minTemp: number;
    let maxTemp: number;
    if (fanData[0] == 0) {
        fanSpeed(0)
    } else if (fanData[0] == 1) {
        fanSpeed(fanData[1])
    } else if (fanData[0] == 2) {
        fanSpeed(fanData[1])
        if (fanData[2] == ds.getHour() && fanData[3] == ds.getMinute()) {
            changeMode(0)
        }
        
    } else if (fanData[0] == 3 || 4) {
        temperature = dht11_dht22.readData(dataType.temperature)
        minTemp = fanData[4]
        maxTemp = fanData[5]
        if (temperature <= minTemp) {
            fanSpeed(0)
        } else if (temperature >= maxTemp) {
            fanSpeed(9)
        } else {
            fanSpeed(Math.trunc((temperature - minTemp) / (maxTemp - minTemp) * 9))
        }
        
        if (fanData[0] == 4) {
            if (fanData[2] == ds.getHour() && fanData[3] == ds.getMinute()) {
                changeMode(0)
            }
            
        }
        
    }
    
    basic.pause(2000)
})
function fanSpeed(speed: number) {
    pins.analogWritePin(AnalogPin.P4, 348 + speed * 75)
    if (speed == 0) {
        pins.analogWritePin(AnalogPin.P4, 0)
    }
    
}

led.enable(false)
let fanData = [0, 5, 0, 1, 10, 15]
makerbit.connectIrReceiver(DigitalPin.P0, IrProtocol.Keyestudio)
let ds = DS1302.create(DigitalPin.P13, DigitalPin.P14, DigitalPin.P15)
dht11_dht22.queryData(DHTtype.DHT11, DigitalPin.P1, true, false, false)
radio.setGroup(1)
