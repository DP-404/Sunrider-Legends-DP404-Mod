import os
import shutil

import _utility as utility

TEXT_EXPORTED = 'Exported: {Filename}'
PATH_EXPORT = os.path.join(os.path.dirname(utility.DATA_PATH), "exported_data")
PATH_DEFAULT = os.path.join(PATH_EXPORT, "default")
PATH_DECODED = os.path.join(PATH_EXPORT, "decoded")
PATH_DEBUG = os.path.join(PATH_EXPORT, "debug")

def export(filename:str):
    path = os.path.join(utility.DATA_PATH, filename)
    export_path_default = os.path.join(PATH_DEFAULT, filename)
    export_path_decoded = os.path.join(PATH_DECODED, filename)
    export_path_debug = os.path.join(PATH_DEBUG, filename)

    text = utility.load_text(path)
    _,worklines = utility.split_text_lines(text)
    _,worklines_debug = utility.split_text_lines(text, debug=True)
    export_text = '\n'.join(worklines)
    export_text_debug = '\n'.join(worklines_debug)

    utility.save_text(export_path_default, export_text, b64encode=True)
    utility.save_text(export_path_decoded, export_text)
    utility.save_text(export_path_debug, export_text_debug, b64encode=True)

    print(TEXT_EXPORTED.format(Filename=filename))

def export_all():
    for filename in utility.DATA_FILES:
        export(filename)
    if os.path.exists(utility.STEAM_PATH):
        for filename in os.listdir(PATH_DECODED):
            shutil.copy(
                os.path.join(PATH_DEFAULT, filename),
                os.path.join(utility.STEAM_PATH, filename)
            )

if __name__ == '__main__':
    export_all()
