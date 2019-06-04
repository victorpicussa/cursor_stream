#!python3

import socket
import logging
import pickle
import sys
import time
import settings

# Cursor librarys
import pyautogui
from pynput import mouse, keyboard
from pynput.mouse import Button, Controller

logging.basicConfig(format = settings.LOGGING_FORMAT, level = settings.LOGGING_LEVEL, datefmt = settings.LOGGING_DFT)
logger = logging.getLogger(__name__)

# Packet structure
data = {
    'id'    : 0,
    'mouse_position' : (0,0),
    'mouse_pressed' : False,
    'mouse_scrolled' : False,
    'screen_size' : (0, 0),
}

# Connection initialization function
def connection(PORT, GROUP, TTL):
    host_name = socket.gethostname()
    host = socket.gethostbyname(host_name)

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, TTL)
        logger.info('Socket created')
    except:
        logger.error('Error on socket creation')
        exit(0)

    return sock

def on_move(x, y):
    data['mouse_position'] = (x,y)
    logger.debug('Pointer moved to {0}'.format((x, y)))

def on_click(x, y, button, pressed):
    data['mouse_pressed'] = pressed
    logger.debug('{0} at {1}'.format('Pressed' if pressed else 'Released', (x, y)))

def on_scroll(x, y, dx, dy):
    data['mouse_scrolled'] = True
    logger.debug('Scrolled {0} at {1}'.format('down' if dy < 0 else 'up', (x, y)))

def init(argv):
    if '--help' in argv:
        print('Usage: ' + settings.MESSAGES['usage_server'])
        exit(0)

    # Verify if any option is in the arguments
    if '-p' in argv:
        port = int(argv[argv.index('-p') + 1])
    else:
        port = settings.DEFAULT_MCAST_PORT
    if '-t' in argv:
        ttl = int(argv[argv.index('-t') + 1])
    else:
        ttl = settings.DEFAULT_MCAST_TTL
    if '-g' in argv:
        grp = int(argv[argv.index('-g') + 1])
    else:
        grp = settings.DEFAULT_MCAST_GRP

    try:
        sock = connection(port, grp, ttl)
        logger.info('Socket connection succeeded')
    except:
        logger.error('Error on socket connection')
        exit(0)

    # Send data until CTRL + C
    try:
        counter = 0
        # Collect events until released
        listener = mouse.Listener(
                on_move=on_move, 
                on_click=on_click, 
                on_scroll=on_scroll)
        try:
            listener.start()
            logger.info('Mouse listener started')
        except:
            loggin.error('Mouse listener start failed')
            exit(0)
        

        screen_w, screen_h = pyautogui.size()
        try:
            data['id'] = counter
            data['screen_size'] = (screen_w, screen_h)
            time.sleep(0.0001)
            sock.sendto(pickle.dumps(data), (grp, port))
            data['id'] = counter
            data['mouse_scrolled'] = False
            counter += 1
            logger.info('First packet sent succefuly')
        except:
            logger.error('Sending packet failed')
            exit(0)

        while True:
            time.sleep(0.0001)
            sock.sendto(pickle.dumps(data), (grp, port))
            data['id'] = counter
            data['mouse_scrolled'] = False
            counter += 1
    except KeyboardInterrupt:
        logger.info('Last packet sent id:%d', data['id'])
        listener.stop()
        logger.info('Mouse listener closed')
        logger.info('Closing server')
        exit(1)

init(sys.argv)