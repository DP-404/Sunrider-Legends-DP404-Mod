import os

import _utility as utility

TEXT_EXPORTED = 'Exported: {Filename}'

def export(filename:str):
    path = os.path.join(utility.DATA_PATH, filename)
    export_path = os.path.join(os.path.dirname(utility.DATA_PATH), filename)

    text = utility.load_text(path)
    _,worklines = utility.split_text_lines(text)
    text = '\n'.join(worklines)

    utility.save_text(export_path, text, b64encode=True)
    print(TEXT_EXPORTED.format(Filename=filename))

def export_all():
    for filename in utility.DATA_FILES:
        export(filename)

if __name__ == '__main__':
    export_all()
