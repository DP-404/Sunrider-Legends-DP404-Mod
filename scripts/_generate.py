import os

import _utility as utility

TEXT_GAME_404 = "Game path not found: {Path}"
TEXT_DATA_GENERATED = "Data generated."

PATH_GENERATE = os.path.join(utility.BASE_PATH, "generated_data")

def generate():
    game_path = utility.STEAM_PATH

    if os.path.exists(game_path) and len(os.listdir(game_path)) == 0:
        print(TEXT_GAME_404.format(Path=game_path))
        return

    for fn in [
        i
        for i in os.listdir(game_path)
        if i.startswith(utility.SOURCE_LANGUAGE) and i.endswith('.txt')
    ]:
        txt = utility.load_text(os.path.join(game_path, fn), b64decode=True)
        new_txt_lns = []
        for ln in txt.split('\n'):
            new_txt_lns.append(utility.TEMPLATE_MARK + " " + ln)
            new_txt_lns.append(ln)
        new_txt = '\n'.join(new_txt_lns)
        new_fn = fn.replace(utility.SOURCE_LANGUAGE, utility.LANGUAGE)
        utility.save_text(os.path.join(PATH_GENERATE, new_fn), new_txt)
    print(TEXT_DATA_GENERATED)

if __name__ == "__main__":
    generate()