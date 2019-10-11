TEXT_WHITE = '\u001b[37;1m'
TEXT_BLACK = '\u001b[30;1m'
TEXT_RED = '\u001b[31;1m'  
TEXT_BLUE = '\u001b[34;1m'
TEXT_CYAN = '\u001b[36;1m'
TEXT_MAGENTA = '\u001b[35;1m'
TEXT_GREEN = '\u001b[32;1m'
TEXT_YELLOW = '\u001b[33;1m'

BG_WHITE = '\u001b[47;1m'
BG_BLACK = '\u001b[40;1m'
BG_RED = '\u001b[41;1m'  
BG_BLUE = '\u001b[44;1m'
BG_CYAN = '\u001b[46;1m'
BG_MAGENTA = '\u001b[45;1m'
BG_GREEN = '\u001b[42;1m'
BG_YELLOW = '\u001b[43;1m'

RESET = '\u001b[0m'


def text_color(option):
    switcher = {
        'white': TEXT_WHITE,
        'black': TEXT_BLACK,
        'red': TEXT_RED,
        'blue': TEXT_BLUE,
        'cyan': TEXT_CYAN,
        'magenta': TEXT_MAGENTA,
        'green': TEXT_GREEN,
        'yellow': TEXT_YELLOW
    }

    return switcher.get(option, '')

def background_color(option):
    switcher = {
        'white': BG_WHITE,
        'black': BG_BLACK,
        'red': BG_RED,
        'blue': BG_BLUE,
        'cyan': BG_CYAN,
        'magenta': BG_MAGENTA,
        'green': BG_GREEN,
        'yellow': BG_YELLOW
    }

    return switcher.get(option, '')

def reset_formatting():
    return RESET
