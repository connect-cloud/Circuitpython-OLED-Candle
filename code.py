import board, busio, displayio, time
from adafruit_displayio_sh1107 import SH1107, DISPLAY_OFFSET_PIMORONI_MONO_OLED_PIM374
import adafruit_imageload

IMAGE_FILE = "fire.bmp"
SPRITE_SIZE = (128, 128)
FRAMES = 28

def invert_colors():
    temp = icon_pal[0]
    icon_pal[0] = icon_pal[1]
    icon_pal[1] = temp

# Display init
displayio.release_displays()
i2c = board.STEMMA_I2C()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)

WIDTH = 128
HEIGHT = 128
BORDER = 2
ROTATION = 270

display = SH1107(
    display_bus, width = WIDTH, height = HEIGHT, rotation = ROTATION,
    display_offset=DISPLAY_OFFSET_PIMORONI_MONO_OLED_PIM374
)
group = displayio.Group()

#  load the spritesheet
icon_bit, icon_pal = adafruit_imageload.load(IMAGE_FILE,
                                                 bitmap=displayio.Bitmap,
                                                 palette=displayio.Palette)
invert_colors()

icon_grid = displayio.TileGrid(icon_bit, pixel_shader=icon_pal,
                                 width=1, height=1,
                                 tile_height=SPRITE_SIZE[1], tile_width=SPRITE_SIZE[0],
                                 default_tile=0,
                                 x=0, y=0)

group.append(icon_grid)

display.show(group)

timer = 0
pointer = 0

while True:
  if (timer + 0.08) < time.monotonic():
    icon_grid[0] = pointer
    pointer += 1
    timer = time.monotonic()
    if pointer > FRAMES-1:
      pointer = 0
