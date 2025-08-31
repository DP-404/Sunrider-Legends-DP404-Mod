import os

import _utility as utility

TEXT_EXPORTED = 'Exported: {Filename}'
EXPORT_PATH = os.path.join(os.path.dirname(utility.DATA_PATH), "exported_data")

def export(filename:str):
    path = os.path.join(utility.DATA_PATH, filename)
    export_path = os.path.join(EXPORT_PATH, "default", filename)
    export_path_decoded = os.path.join(EXPORT_PATH, "decoded", filename)
    export_path_debug = os.path.join(EXPORT_PATH, "debug", filename)

    text = utility.load_text(path)
    _,worklines = utility.split_text_lines(text)
    _,worklines_debug = utility.split_text_lines(text, debug=True)
    export_text = '\n'.join(worklines)
    export_text_debug = '\n'.join(worklines_debug)

    utility.save_text(export_path, export_text, b64encode=True)
    utility.save_text(export_path_decoded, export_text)
    utility.save_text(export_path_debug, export_text_debug, b64encode=True)

    print(TEXT_EXPORTED.format(Filename=filename))

def export_all():
    for filename in utility.DATA_FILES:
        export(filename)

if __name__ == '__main__':
    export_all()
