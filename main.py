import time
import board
import neopixel

pixels = neopixel.NeoPixel(board.D4, 75, brightness=1.0, auto_write=False)

# Color constants
RED = ((200, 0, 0), (1, 0, 0))
ORANGE = ((255, 128, 0), (10, 6, 0))
YELLOW = ((150, 107, 0), (15, 10, 0))
GREEN = ((0, 200, 0), (0, 1, 0))
AQUA = ((0, 140, 140), (0, 1, 1))
BLUE = ((0, 0, 200), (0, 0, 1))
PURPLE = ((140, 0, 140), (1, 0, 1))
WHITE = ((200, 200, 200), (10, 10, 10))
BLACK = (0, 0, 0)

# light section ranges
light_bottom = range(10, -1, -1)
light_right = range(11, 30)
light_plug = range(30, 33)
light_left = range(33, 52)
light_middle = range(52, 63)
light_top = range(63, 75)

side_lights = list(light_right) + list(light_left)

# the vertical lights as 1-dimensional arrays
vertical_up = list(light_bottom) + list(light_middle) + list(light_top)
vertical_down = list(light_top[::-1]) + list(light_middle[::-1]) + list(light_bottom[::-1])
vertical_lower_half = vertical_up[:len(vertical_up)//2]
vertical_upper_half = vertical_up[len(vertical_up)//2:]

# Start by blanking the whole lamp
pixels.fill(BLACK)

# Higher numbers are faster, lower numbers are slower
# Give it 5, the delay between updates will be .01
# 7 is .006
# 2 is .016
def wait(speed):
    if (speed > 9):
        speed = 9
    elif (speed < 0):
        speed = 0
    time.sleep((10 - speed) / 200)

plug_iter = 0
plug_range = list(range(30, 150, 6)) + list(range(150, 30, -6))
def animate_plug(color):
    global plug_iter
    for i in light_plug:
        pixels[i] = (plug_range[plug_iter], plug_range[plug_iter], plug_range[plug_iter])
        
    plug_iter += 1
    
    if (plug_iter == len(plug_range)):
        plug_iter = 0

side_light_iter = 0
def run_back(color):
    animate_plug(color)
    global side_light_iter
    side_light_iter += 1
    if (side_light_iter < len(light_right)):
        pixels[light_right[side_light_iter]] = color[0]
        pixels[light_left[side_light_iter]] = color[0]
        pixels[light_right[side_light_iter - 1]] = color[1]
        pixels[light_left[side_light_iter - 1]] = color[1]
    else:
        side_light_iter = 0

def run_scissor_out(color, speed):
    for i, pixel in enumerate(vertical_upper_half):
        run_back(color)
        if (len(vertical_lower_half) - 2 - i >= 0):
            pixels[vertical_lower_half[len(vertical_lower_half) - 2 - i]] = color[0]
        pixels[pixel] = color[0]
        if (i < len(vertical_lower_half)):
            pixels[vertical_lower_half[len(vertical_lower_half) - 1 - i]] = color[1]
            pixels[vertical_upper_half[i - 1]] = color[1]
        pixels.show()
        wait(speed)

def run_scissor_in(color, speed):
    for i, pixel in enumerate(vertical_lower_half):
        run_back(color)
        if (len(vertical_upper_half) - 2 - i >= 0):
            pixels[vertical_upper_half[len(vertical_upper_half) - 2 - i]] = color[0]
        pixels[pixel] = color[0]
        if (i >= 0 & i < len(vertical_lower_half)):
            pixels[vertical_upper_half[len(vertical_upper_half) - 1 - i]] = color[1]
            pixels[vertical_lower_half[i - 1]] = color[1]
        pixels[vertical_lower_half[-1]] = color[1]
        pixels.show()
        wait(speed)

def fill(pixel_range, color, speed):
    for pixel in pixel_range:
        run_back(color)
        pixels[pixel] = color[0]
        pixels.show()
        wait(speed)

def fill_up(color, speed):
    fill(vertical_up, color, speed)
    
def fill_down(color, speed):
    fill(vertical_down, color, speed)

def erase(pixel_range, color, speed):
    for i, pixel in enumerate(pixel_range):
        run_back(color)
        if (i > 0):
            pixels[pixel_range[i - 1]] = color[1]
        pixels.show()
        wait(speed)

def erase_down(color, speed):
    erase(vertical_down, color, speed)

def erase_up(color, speed):
    erase(vertical_up, color, speed)

def run(pixel_range, color, speed):
    for i, pixel in enumerate(pixel_range):
        run_back(color)
        pixels[pixel] = color[0]
        pixels[pixel_range[i - 1]] = color[1]
        pixels.show()
        wait(speed)

def run_up(color, speed):
    run(vertical_up, color, speed)

def run_down(color, speed):
    run(vertical_down, color, speed)

def chase_down(color, speed):
    for i, pixel in enumerate(vertical_down):
        run_back(color)
        pixels[pixel] = color[0]
                
        if (i > 0):
            pixels[vertical_down[i - 1]] = color[1]
            
        wait(speed)
        pixels.show()
    pixels[vertical_down[-1]] = color[1]
    pixels.show()

def pulse(color, speed):
    # This range is the light intensity percentage and the steps in between. 
    #  Right now it's fading between 20% and 85% of the color's max intensity, 
    #  incrementing in steps of 3%
    for i in list(range(20, 85, 3)) + list(range(85, 20, -3)):
        percent = i / 100
        run_back(color)
        fade = (int(color[0][0] * percent), int(color[0][1] * percent), int(color[0][2] * percent))
        
        for pixel in (vertical_up):
            pixels[pixel] = fade
        
        pixels.show()

def test_pattern(color, speed):
    fill_down(color, 9)
    erase_up(color, 9)

#     run_down(color, 9)
#     run_up(color, 9)
#     run_scissor_out(color, 9)
#     run_scissor_in(color, 9)
#     pulse(color, 9)
#     chase_down(color, 9)
#     fill_up(color, 9)
#     erase_down(color, 9)

while True:
    try:
        with open("/animation.txt", "r") as fp:
            for line in fp:
                print(line.rstrip())
                eval(line)

    except OSError as e:
        delay = 0.5
        if e.args[0] == 28:
            delay = 0.25
        while True:
            time.sleep(delay)
