# ow_gpio
One wire platform for ESPHOME that doesn't lock interrupts for the full 64 bit sensor address at once but only for every single bit. In this way preventing cheap display glitches on e.g.  ESP32-8048S050 displays when combined with a DS18B20

The standard 1-Wire driver blocks interrupts for an entire byte, and for the full 64-bit sensor address at once for a DS18B20. Sending that address takes about 4 ms. The screen refresh needs an interrupt roughly every 0.6 ms to keep feeding the panel, so each sensor read starves it and you see a glitch.

1-Wire only needs exact timing within each single bit (about 70 µs); the gaps between bits can be any length. I've made a copy of ESPHome's driver, ow_gpio, that blocks interrupts one bit at a time. The longest block is now about 300 µs during the reset pulse, which leaves room for the screen. The protocol and the DS18B20 handling are otherwise the same.

To install it, put the four files into your ESPHome config folder like this:

/config/esphome/components/ow_gpio/__init__.py
/config/esphome/components/ow_gpio/one_wire.py
/config/esphome/components/ow_gpio/ow_gpio.h
/config/esphome/components/ow_gpio/ow_gpio.cpp

In your ESPHOME config use:

external_components:
  - source:
      type: local
      path: components

one_wire:
  - platform: ow_gpio        # was: gpio
    pin: ${onewire_pin}
