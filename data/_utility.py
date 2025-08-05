import base64
import os
from traceback import format_exc
from typing import Any, Callable

ENCODING = 'utf8'
DATA_PATH = os.path.dirname(__file__)
DATA_FILES = [
    f
    for f in os.listdir(DATA_PATH)
    if f.endswith('.txt')
]
TEMPLATE_MARK = '#'
PROGRESS_MARK = '%'
COMMANDS = [
    '//', 'bat', 'ccc', 'cha', 'dcg', 'dbg', 'fade', 'flag', 'hid', 'ifj', 'mus',
    'obj', 'roo', 'sou', 'stop', 'tag', 'var', 'voi', 'xob'
]

def load_text(path:str, b64decode:bool=False):
    with open(path, encoding=ENCODING) as file:
        text = file.read()
    lns = text.split('\n')
    if b64decode == True:
        lns = [
            base64.b64decode(ln).decode(encoding=ENCODING)
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

def split_text_lines(text:str):
    templates:list[str] = []
    worklines:list[str] = []
    lns = text.split('\n')
    i = 0
    while i < len(lns):
        ln = lns[i]
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
