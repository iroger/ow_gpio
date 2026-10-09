"""Low-latency GPIO 1-Wire bus: same as `platform: gpio`, but interrupts are only
blocked for one bit slot at a time (~70 us) instead of a whole byte or the
64-bit ROM address (~4 ms), which starves the RGB panel's bounce-buffer refills."""

from esphome import pins
import esphome.codegen as cg
from esphome.components.one_wire import OneWireBus
import esphome.config_validation as cv
from esphome.const import CONF_ID, CONF_PIN

from . import ow_gpio_ns

LowLatencyOneWireBus = ow_gpio_ns.class_("LowLatencyOneWireBus", OneWireBus, cg.Component)

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(LowLatencyOneWireBus),
        cv.Required(CONF_PIN): pins.internal_gpio_output_pin_schema,
    }
).extend(cv.COMPONENT_SCHEMA)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    pin = await cg.gpio_pin_expression(config[CONF_PIN])
    cg.add(var.set_pin(pin))
