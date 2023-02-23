input.onButtonPressed(Button.A, function on_button_pressed_a() {
    fanData[1] = Math.trunc(fanData[1] / 3) * 3 % 9 + 3
})
input.onButtonPressed(Button.B, function on_button_pressed_b() {
    fanData[0] = (fanData[0] + 1) % 4
    pins.digitalWritePin(DigitalPin.P8, 0)
    pins.digitalWritePin(DigitalPin.P9, 0)
    pins.digitalWritePin(DigitalPin.P10, 0)
    if (fanData[0] == 1) {
        pins.digitalWritePin(DigitalPin.P9, 1)
    } else if (fanData[0] == 2) {
        pins.digitalWritePin(DigitalPin.P10, 1)
        ds.setSecond(0)
        ds.setMinute(0)
        ds.setHour(0)
    } else if (fanData[0] == 3) {
        pins.digitalWritePin(DigitalPin.P8, 1)
    }
    
})
basic.forever(function on_forever() {
    if (fanData[0] == 3) {
        
    } else if (fanData[0] == 2) {
        
    } else if (fanData[0] == 1) {
        fanSpeed(fanData[1])
    } else if (fanData[0] == 0) {
        fanSpeed(0)
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
let fanData = [0, 5, 2, 30, 20, 30]
makerbit.connectIrReceiver(DigitalPin.P0, IrProtocol.Keyestudio)
let ds = DS1302.create(DigitalPin.P13, DigitalPin.P14, DigitalPin.P15)
dht11_dht22.queryData(DHTtype.DHT11, DigitalPin.P1, true, false, false)
