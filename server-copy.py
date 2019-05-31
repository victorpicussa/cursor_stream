#!python3

import socket
import pyautogui
import logging
import pickle
import sys

from Xlib import X, XK, display
from Xlib.ext import record
from Xlib.protocol import rq

local_dpy = display.Display()
record_dpy = display.Display()


# Default variables
DEFAULT_MCAST_GRP = '224.1.1.1'
DEFAULT_MCAST_PORT = 5007
DEFAULT_MCAST_TTL = 2
MESSAGES = {
    'usage': '<server> [[-p <port>], [-t <ttl>], [-g <group>]]' 
}

# Connection initialization function
def connection(PORT, GROUP, TTL):
    host_name = socket.gethostname()
    host = socket.gethostbyname(host_name)

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, TTL)
    except:
        print("Erro ao criar socket!")
        exit(0)

    return sock

def initRecorder(reply):
    if reply.category != record.FromServer:
        return
    if reply.client_swapped:
        print ("* received swapped protocol data, cowardly ignored")
        return
    if not len(reply.data) or ord(reply.data[0]) < 2:
        # not an event
        return
    return reply.data

def logger(data):
    # For debug purposes
    positionStr = 'X: ' + str(data['X_pos']).rjust(4) + ' Y: ' + str(data['Y_pos']).rjust(4)
    print(positionStr, end='')
    print('\b' * len(positionStr), end='', flush=True)

def getCursor(counter):
    # Cursor positions and window size data
    x, y = pyautogui.position()
    w, h = pyautogui.size()
    data = {
        'id'    : counter,
        'X_pos' : x,
        'Y_pos' : y,
        'width' : w,
        'height': h
    }
    return data 

def init(argv):
    if '--help' in argv:
        print('Usage: ' + MESSAGES['usage'])
        exit(0)

    # Verify if any option is in the arguments
    if '-p' in argv:
        port = int(argv[argv.index('-p') + 1])
    else:
        port = DEFAULT_MCAST_PORT
    if '-t' in argv:
        ttl = int(argv[argv.index('-t') + 1])
    else:
        ttl = DEFAULT_MCAST_TTL
    if '-g' in argv:
        grp = int(argv[argv.index('-g') + 1])
    else:
        grp = DEFAULT_MCAST_GRP

    sock = connection(port, grp, ttl)
    
    # Send data until CTRL + C
    try:
        counter = 0
        recorder_data = initRecorder()
        while True:
            data = getCursor(counter)
            logger(data)
            sock.sendto(pickle.dumps(data), (grp, port))
            counter += 1
    except KeyboardInterrupt:
        print('\nFinalizando servidor...')
        exit(1)

init(sys.argv)