import os

import _utility as utility

class Progress:
    PROGRESS_LINE = "{Filename:<30} : {TotalProgress:>5}/{TotalCount:>5} [{Completion:>6.2f}%]"
    TOTAL_PROGRESS = "TOTAL PROGRESS"

    def __init__(self, filename:str=TOTAL_PROGRESS, total_count:int=0, total_progress:int=0, total_nocount:int=0):
        self.filename = filename
        self.total_count = total_count - total_nocount
        self.total_progress = total_progress - total_nocount
        self.total_cmd = total_nocount

    @property
    def completion(self):
        return round(self.total_progress / self.total_count * 100, 2)

    def print(self):
        print(self.PROGRESS_LINE.format(
            Filename=self.filename,
            TotalProgress=self.total_progress,
            TotalCount=self.total_count,
            Completion=self.completion
        ))

def get_progress(filename:str):
    path = os.path.join(utility.DATA_PATH, filename)
    text = utility.load_text(path)
    templates, worklines = utility.split_text_lines(text)

    total_count = len(templates)
    total_progress = 0
    total_nocount = 0

    i = 0
    progressed = False
    while i < total_count:
        template_line = templates[i]
        work_line = worklines[i]
        plain_line = utility.get_plain_line(template_line)
        is_cmd = utility.is_line_command(plain_line)
        is_empty = plain_line.strip() == ''

        if is_cmd or is_empty:
            total_nocount += 1

        if utility.is_line_progressed(template_line):
            total_progress += 1
        elif (
            plain_line != work_line
            or is_cmd
            or is_empty
        ):
            total_progress += 1
            progressed = True
            template_line = utility.mark_line_as_progressed(template_line)
            templates[i] = template_line
        i += 1

    if progressed:
        new_text = utility.join_text_lines(templates, worklines)
        utility.save_text(path, new_text)

    return Progress(filename, total_count, total_progress, total_nocount)

def get_all_progresses():
    progresses = [
        get_progress(filename)
        for filename in utility.DATA_FILES
    ]
    progresses.append(
        Progress(
            total_count=sum([p.total_count for p in progresses]),
            total_progress=sum([p.total_progress for p in progresses]),
        )
    )
    return progresses

def print_progress():
    progresses = get_all_progresses()
    for p in progresses:
        p.print()

if __name__ == '__main__':
    print_progress()
