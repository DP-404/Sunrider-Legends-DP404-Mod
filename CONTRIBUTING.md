# Developer Guide

These are some guidelines as to how to work with the project for developers' usage.

---

## Project Structure

- `data/`: The data files which you'll modify when working on your project.
- `exported_data/`: The exported data files are saved here.
- `generated_data/`: Brand new generated data files are saved here.
- `Localization/`: This folder is to be packaged alongside the script files. Herein lies the language settings.
- `scripts/`: Some Python scripts used for handling the project easier.
- `source_data/`: You may place specific original data files here to be used as reference for the tools. If you don't have any files here, the Steam game path will be resolved and used instead of this.

---

## Data Scripts

The data scripts located within the `data/` folder have their own semantic. Let's look at this example:

```
1: #% tag random_event
2: tag random_event
3: # foo The quick brown fox jumps over the lazy dog.
4: foo The quick brown fox jumps over the lazy dog.
5: #% bar Pack my box with five dozen liquor jugs.
6: bar Empaqueta mi caja con cinco docenas de jarras de licor.
7: #% &debug
8: jum end_event
```

The lines starting with `#` are the original script lines (lines 1, 3, 5... they will always be odd numbers) and the lines right below are the custom lines (lines 2, 4, 6...). Original lines should not be modified, as they are supposed to be a guide for you to know what you are changing in the custom lines as you do it and they are also used to check for differences between the working project and any script updates the actual game files may have received. We shall call "entry" to the set of an original script line and its custom line right below.

If a `#` is followed by a `%`, then that line is marked as "progressed" (lines 1, 5). This mark is used by the Progress script as an indicator to know what custom lines have been modified. When using tools, custom lines are compared to their original lines, and if modified, the original line is automatically marked as progressed (line 5). An exception is a command line (these start with specific sequences of characters), which are automatically marked as progressed even when unmodified (line 1). Once marked as progressed, lines are not unmarked even if they return to their original state.

You may add your own entries to the data scripts if you wish so. If your entry's original line is `&debug` (line 7), it will be considered a special entry which will not be included in a usual export.

---

## Python Scripts

The Python modules included in `scripts/` are a set of programs to help managing the project.

- `_utility.py`: This is not a standalone script, but a module with common functions and constants used by the other tools.
- `_diff.py`: Checks for differences between the working data files located in `/data` folder and the original game script files, in order to keep the script files up to date with game updates if any were to change them. The original game files path may refer to either `source_data/` if there are any files therein or to the Steam game path, the first taking priority over the later if its condition is met.
- `_export.py`: Exports the working data files to the `/exported_data` folder. There are different exported data folders herein:
  - `default/`: The encoded script files, ready to be added to the game. These are the ones supposed to be packaged for releases.
  - `decoded/`: The decoded script files. They are exactly the same as the one in `default/`, but decoded so that the final files can be read to know what exactly is being exported.
  - `debug/`: The encoded script files including the debug commands, ready to be added to the game.
- `_generate.py`: Generates a brand new set of data files from the original game files in your system (uses Steam path). These files are ready to be moved to `data/` path and work with them.
- `_pack.py`: Creates a compressed file with the exported files and Localization folder, ready to be distributed and
- `_progress.py`: Shows the progress per script and total in number of lines and percentage.
