from colorama import Back, Fore, Style

colors = {
    'Blue': '\x1b[0;34m',
    'Green': '\x1b[0;32m',
    'Cyan': '\x1b[0;36m',
    'Red': '\x1b[0;31m',
    'Purple': '\x1b[0;35m',
    'Brown': '\x1b[0;33m',
    'Gray': '\x1b[0;37m',
    'lGreen': '\x1b[1;32m',
    'Light Cyan': '\x1b[1;36m',
    'Yellow': '\x1b[1;33m',
    'White': '\x1b[1;37m'
}
RESET = '\x1b[0m'


# Define scene height(vertical), width(horizontal),
# fullwidth(map length)
# These measurements are from the top
sc_top = 4
default_base = 38
sc_height = 40
sc_span = 100
# game length
sc_full = 1500

# GAME TIME LIMIT (s)
sc_time = 5000

# MANDO config

mando_h = 3
mando_w = 3
mx = 34
my = 4