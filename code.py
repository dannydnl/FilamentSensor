import board
import analogio
import time
import busio
import os
import terminalio
import displayio
import microcontroller
import adafruit_displayio_ssd1306
from adafruit_display_text import label


diameter = 0

displayio.release_displays()
i2c = busio.I2C(board.GP1, board.GP0)

display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

# Make the display context
splash = displayio.Group()
display.root_group = splash

color_bitmap = displayio.Bitmap(128, 64, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF  # White

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(126, 62, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0x000000  # Black
inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=1, y=1)
splash.append(inner_sprite)

diameter_string = f"{diameter}mm"

# Draw a label
#text = "Hello World!"
#text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=28, y=28)
#splash.append(text_area)
adc = analogio.AnalogIn(board.GP28)

# Draw the temperature value label
diameter_value_label = label.Label(terminalio.FONT, text = diameter_string, color = 0xFFFFFF)
diameter_value_label.anchor_point = (0.5, 0.5) # Change anchor point to center
diameter_value_label.anchored_position = (64, 38)
diameter_value_label.scale = 3
splash.append(diameter_value_label)

def get_voltage(pin):
    return (pin.value * 3.3) / 65536


while True:
    adc_val = (adc.value * 3.3) / 65536
    diameter = adc_val
    diameter_string = f"{diameter:.2f}mm"
    diameter_value_label.text = diameter_string
    print((diameter))
    time.sleep(0.1)
