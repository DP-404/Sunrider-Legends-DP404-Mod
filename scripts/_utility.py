import base64
import os
import string
import configparser
from traceback import format_exc

GAME_NAME = 'Sunrider Legends Tactics'
SOURCE_LANGUAGE = 'English'
LANGUAGE = 'Spanish'
ENCODING = 'utf8'

BASE_PATH = os.path.dirname(os.path.dirname(__file__))
SOURCE_PATH = os.path.join(BASE_PATH, 'source_data')
'''Stores `"{workspaceFolder}/source_data"` if folder exists and there is any file therein.
Otherwise, uses Steam path to the game.'''

_CP = configparser.ConfigParser()
_CP.read(os.path.join(BASE_PATH, "scripts", "config.cfg"))
STEAM_PATH = _CP.get("main", "STEAM_PATH")

if (
    STEAM_PATH is None
    or len(STEAM_PATH) == 0
    or not os.path.exists(STEAM_PATH)
):
    STEAM_PATH = ""
    disk_unit = os.environ.get('ProgramFiles(x86)')
    if disk_unit is not None:
        STEAM_PATH = os.path.join(
            disk_unit, "Steam", "steamapps", "common", f"{GAME_NAME}"
        )
    if not os.path.exists(STEAM_PATH):
        for disk_unit in string.ascii_letters.upper():
            STEAM_PATH = os.path.join(
                disk_unit+":"+os.sep, "Steam", "steamapps", "common", f"{GAME_NAME}"
            )
            if os.path.exists(STEAM_PATH):
                break
            STEAM_PATH = ""

if not os.path.exists(SOURCE_PATH) or len(os.listdir(SOURCE_PATH)) <= 1:
    SOURCE_PATH = STEAM_PATH
    if not os.path.exists(SOURCE_PATH):
        SOURCE_PATH = ''

VALID_SOURCE = os.path.exists(SOURCE_PATH)

DATA_PATH = os.path.join(BASE_PATH, 'data')
DATA_FILES = [
    f
    for f in os.listdir(DATA_PATH)
    if f.endswith('.txt')
]
SOURCE_DATA_FILES = [
    f
    for f in os.listdir(SOURCE_PATH)
    if f.startswith(SOURCE_LANGUAGE) and f.endswith('.txt')
]

LOCALIZATION_PATH = os.path.join(BASE_PATH, "Localization")

TEMPLATE_MARK = '#'
PROGRESS_MARK = '%'
DEBUG_CMD = '&debug'
COMMANDS = [
    '//', '-1000',
    'bat',
    'ccc', 'cc0', 'cc1', 'cc2', 'cc3', 'cc4', 'cc5', 'cha', 'cre', 'cva',
    'dcg', 'dbg',
    'fade', 'flag',
    'hid', 'hsh',
    'ifj',
    'jum',
    'map', 'mus',
    'obj',
    'par', 'por', 'ptf', 'ptt',
    'roo',
    'sav', 'sou', 'spr', 'stop',
    'tag',
    'var', 'voi',
    'xcr', 'xob',
    DEBUG_CMD
]

def assert_path(path:str):
    if not os.path.isdir(path):
        path = os.path.dirname(path)
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def b64pad(string:str):
    return string + "=" * ((4 - len(string) % 4) % 4)

def load_text(path:str, b64decode:bool=False):
    with open(path, encoding=ENCODING) as file:
        text = file.read()
    text = text.replace('\ufeff','')
    lns = text.split('\n')
    if b64decode == True:
        lns = [
            base64.b64decode(b64pad(ln)).decode(encoding=ENCODING)
            for ln in lns
        ]
    text = '\n'.join(lns)
    return text

def save_text(path:str, text:str, b64encode:bool=False):
    if b64encode == True:
        lns = text.split('\n')
        lns = [
            base64.b64encode(bytes(ln, encoding=ENCODING)).decode(encoding=ENCODING)
            for ln in lns
        ]
        text = '\n'.join(lns)
    assert_path(path)
    with open(path, 'w', encoding=ENCODING) as file:
        saved = file.write(text)
    return saved

def is_line_command(ln:str):
    return ln.startswith(tuple(COMMANDS))

def is_line_template(ln:str):
    return ln.startswith(TEMPLATE_MARK + ' ')

def is_line_progressed(ln:str):
    return ln.startswith(TEMPLATE_MARK + PROGRESS_MARK + ' ')

def mark_line_as_progressed(ln:str):
    return ln.replace(TEMPLATE_MARK + ' ', TEMPLATE_MARK + PROGRESS_MARK + ' ', 1)

def get_plain_line(ln:str):
    return ln.lstrip(TEMPLATE_MARK + PROGRESS_MARK)[1:]

def split_text_lines(text:str, debug:bool=False):
    templates:list[str] = []
    worklines:list[str] = []
    lns = text.split('\n')
    i = 0
    skip_debug = False
    while i < len(lns):
        if skip_debug:
            skip_debug = False
            i += 1
            continue

        ln = lns[i]

        if get_plain_line(ln) == DEBUG_CMD:
            if debug == False:
                skip_debug = True
                i += 1
                continue
        if i % 2 == 0:
            templates.append(ln)
        else:
            worklines.append(ln)
        i += 1
    return templates, worklines

def join_text_lines(templates:list[str], worklines:list[str]):
    lns = []
    i = 0
    while i < len(templates):
        lns.append(templates[i])
        lns.append(worklines[i])
        i += 1
    text = '\n'.join(lns)
    return text

if __name__ == '__main__':
    while True:
        try:
            exec_text = input('IN: ')
            exec(exec_text)
        except KeyboardInterrupt:
            break
        except:
            print(format_exc())
