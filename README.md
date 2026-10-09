# ow_gpio
One wire platform for ESPHOME that doesn't lock interrupts for the full 64 bit sensor address at once but only for every single bit. In this way preventing cheap display glitches on e.g.  ESP32-8048S050 displays when combined with a DS18B20
