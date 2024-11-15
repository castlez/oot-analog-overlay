import os
import pygame
import math
import win32api
import win32con
import win32gui
from ctypes import windll, Structure, c_long, byref

WIDTH = 200
HEIGHT = 100
DEADZONE = 0.1

# these are read from config.txt or text is left white
ESS_LOW = 99
ESS_HIGH = -1

WHITE = (255, 255, 255)
GREEN = (0, 212, 81)
RED = (51, 0, 0)
CUR_COLOR = WHITE

class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]


def queryMousePosition():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return [pt.x, pt.y]

def get_analog_vals(js: pygame.joystick.JoystickType):
    """ 
    Display the analog stick values
    gz scales these value from -79 to 80 for some reason
    so we need to normalize the provide -1 to 1 scale to that
    """
    global CUR_COLOR
    global ESS_LOW
    global ESS_HIGH
    ax =  js.get_axis(0)
    if abs(ax) > DEADZONE:
        if ax > 0.0:
            ax = math.floor(80.0 * ax)
        else:
            ax = math.floor(80.0 * ax)
    else:
        ax = 0
    abax = abs(ax)  # for ess calc
    if abax >= ESS_LOW and abax <= ESS_HIGH:
        CUR_COLOR = GREEN
    elif abax < ESS_LOW:
        # should hit this condition every time if no config.txt
        CUR_COLOR = WHITE
    elif abax > ESS_HIGH:
        CUR_COLOR = RED

    ay = js.get_axis(1)
    if abs(ay) > DEADZONE:
        if ay > 0.0:
            ay = math.floor(-79.0 * ay)
        else:
            ay = math.floor(-80.0 * ay)
    else:
        ay = 0
    return f"{ax}        {ay}"

def main():
    global CUR_COLOR
    global ESS_LOW
    global ESS_HIGH

    # check if we have a config.txt for ess high and low
    if os.path.exists("config.txt"):
        lines = []
        with open("config.txt", "r") as f:
            lines = f.readlines()
        if len(lines) == 2:
            elow = -1
            ehigh = -1
            try:
                elow = int(lines[0])
                ehigh = int(lines[1])
            except Exception:
                pass
            if elow != -1 and ehigh != -1:
                ESS_LOW = elow
                ESS_HIGH = ehigh
    
    # env vars
    os.environ['SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS'] = '1'
    os.environ['SDL_VIDEO_WINDOW_POS'] = "20,20"

    # greeting
    print("\n\n=================================================")
    print("Welcome to my little analog stick value overlay!!\n")
    print("Hold left control to move it around (little python console window must be focused)\n")
    print("If the numbers are green, you are within the bounds for ESS position (HESS away!)")
    print("=================================================")

    # init
    pygame.init()
    pygame.joystick.init()
    screen = pygame.display.set_mode((WIDTH,HEIGHT), pygame.NOFRAME) # For borderless, use pygame.NOFRAME
    done = False
    fuchsia = (0, 0, 0)  # Transparency color
    font = pygame.font.Font(None, 45)
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    txt = font.render(get_analog_vals(joysticks[0]), True, CUR_COLOR)

    # Create layered window
    hwnd = pygame.display.get_wm_info()["window"]
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                        win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)

    # Set window transparency color
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)
    x = 0
    y = 0
    win32gui.SetWindowPos(pygame.display.get_wm_info()['window'], -1, x, y, 0, 0, 1)

    # main loop
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LCTRL]:
            # move window around if focused and lctrl is held
            mp = queryMousePosition()
            x = mp[0] - math.floor(WIDTH//2)
            y = mp[1] - math.floor(HEIGHT//2)
            win32gui.SetWindowPos(pygame.display.get_wm_info()['window'], -1, x, y, 0, 0, 1)

        txt = font.render(get_analog_vals(joysticks[0]), True, CUR_COLOR)

        screen.fill(fuchsia)  # Transparent background
        text_rect = txt.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(txt, text_rect)
        pygame.display.update()

if __name__ == "__main__":
    main()
