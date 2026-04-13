import datetime
import os
import zipfile

import _utility as utility
import _export as export

PATH_LOCALIZATION = os.path.join(utility.BASE_PATH, "Localization")
TEXT_PACKING_FINISHED = "Packing finished."

def pack_script(zf:zipfile.ZipFile):
    export_path = export.PATH_DEFAULT
    if not os.path.exists(export_path) or len(os.listdir(export_path)) == 0:
        export.export_all()

    for filename in os.listdir(export.PATH_DEFAULT):
        file_path = os.path.join(export.PATH_DEFAULT, filename)
        if os.path.isfile(file_path):
            zf.write(file_path, filename)

def pack_localization(zf:zipfile.ZipFile):
    for root, _, files in os.walk(utility.LOCALIZATION_PATH):
        for file in files:
            file_path = os.path.join(root, file)
            archive_path_in_zip = os.path.relpath(file_path, utility.LOCALIZATION_PATH)
            zf.write(file_path, os.path.join(os.path.basename(utility.LOCALIZATION_PATH), archive_path_in_zip))

def pack():
    now = datetime.datetime.now()
    fn = now.strftime("%Y-%m-%d-%H-%M-%S") + ".zip"
    zf = zipfile.ZipFile(
        os.path.join(utility.BASE_PATH, fn),
        'w',
        zipfile.ZIP_STORED
    )
    pack_script(zf)
    pack_localization(zf)
    zf.close()

if __name__ == '__main__':
    pack()
    print(TEXT_PACKING_FINISHED)
