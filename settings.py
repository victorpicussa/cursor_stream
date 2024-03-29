# Settings used by the server and client module

import logging

# Default multicast group
DEFAULT_MCAST_GRP = '224.1.1.1'

# Default port
DEFAULT_MCAST_PORT = 5007

# Default TTL
DEFAULT_MCAST_TTL = 2

# Default sent time
DEFAULT_TIME = 0.0001

# Define if will use specific group or all
IS_ALL_GROUPS = True

# File path to save the cursor heatmap graphic
SAVE_CURSOR = 'cursor_heat.jpg'

# File path to save the scrolls heatmap graphic
SAVE_SCROLL = 'scroll_heat.jpg'

# File path to save the clicks heatmap graphic
SAVE_PRESS = 'press_heat.jpg'

# File path to server log
LOGGING_FILE_SERVER = 'server.log'

# File path to client log
LOGGING_FILE_CLIENT = 'client.log'

# Logging definitions
LOGGING_LEVEL = logging.INFO
LOGGING_FORMAT = '%(asctime)s [%(levelname)s]: %(message)s'
LOGGING_DFT = '%m-%d-%Y %H:%M:%S'

# Default messages
MESSAGES = {
    'usage_server': '<server> [[-p <port>], [-t <ttl>], [-g <group>], [-i <seconds>]]',
    'usage_client': '<client> -h <server_name> [[-p <port>], [-g <group>], [-simage]]',
    'descr_server': [
                        '<port>: port where socket will be created',
                        '<ttl>: time to live of the packets',
                        '<seconds>: time between packets sent'
    ],
    'descr_client': {
        'needed': [
            '<server_name>: name of the server that the socket \
                        will be receiving data'
        ],
        'optional': [
            '<port>: port where socket will be created',
            'simage: save the graphics to images folder'
        ]
    }
}
