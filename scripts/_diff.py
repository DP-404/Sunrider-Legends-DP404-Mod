import os

import _utility as utility

MAX_DIFF_COUNT = 5

TEXT_SELECT_GAME_PATH = "Enter game path: "
TEXT_TRY_AGAIN = "Path or source files do not exist. Try again."
TEXT_NEW_DATA = "New data file: {Filename}"
TEXT_MORE = '...'
TEXT_DIFF_DETECTED = 'Diff Detected: {Filename}\n{Diff}\n'
TEXT_DIFF_LINE = '{Ln}/{LnDouble}: [{Text}]'
TEXT_NO_DIFF = 'No Diff Detected.'

def check_diff(filename:str, path:str):
    source_path = os.path.join(path, filename)
    data_path = os.path.join(utility.DATA_PATH, filename.replace(utility.SOURCE_LANGUAGE, utility.LANGUAGE))

    if not os.path.exists(data_path):
        print(TEXT_NEW_DATA.format(Filename=filename))
        return True

    source_text = utility.load_text(source_path, b64decode=True)
    source_lines = source_text.split('\n')
    templates,_ = utility.split_text_lines(utility.load_text(data_path))
    data_lines = [utility.get_plain_line(ln) for ln in templates]

    diff_count = 0
    diff_lines:list[str] = []
    i = 0
    while i < len(source_lines):
        lni = i + 1
        if i >= len(data_lines):
            diff_lines.append(str(lni))
            diff_lines.append(TEXT_MORE)
            break

        sou_ln = source_lines[i]
        dat_ln = data_lines[i]
        if sou_ln != dat_ln:
            diff_lines.append(str(lni))
            diff_count += 1
            if diff_count == MAX_DIFF_COUNT:
                diff_lines.append(TEXT_MORE)
                break
        else:
            diff_count = 0
        i += 1

    diff = len(diff_lines) != 0
    if diff:
        print(TEXT_DIFF_DETECTED.format(
            Filename=filename,
            Diff='\n'.join([
                TEXT_DIFF_LINE.format(
                    Ln=i,
                    LnDouble=int(i) * 2,
                    Text=source_lines[int(i)-1]
                )
                if i.isnumeric()
                else i
                for i in diff_lines
            ])
        ))

    return diff

def check_diff_all():
    if utility.SOURCE_PATH == '':
        while True:
            path = input(TEXT_SELECT_GAME_PATH)
            if (
                os.path.exists(path)
                and all(os.path.exists(os.path.join(path, fn)) for fn in utility.SOURCE_DATA_FILES)
            ):
                break
            print(TEXT_TRY_AGAIN)
    else:
        path = utility.SOURCE_PATH

    diff_detected = False
    for filename in utility.SOURCE_DATA_FILES:
        if check_diff(filename, path):
            diff_detected = True

    if not diff_detected:
        print(TEXT_NO_DIFF)

if __name__ == '__main__':
    check_diff_all()
