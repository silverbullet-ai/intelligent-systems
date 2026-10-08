# Smart Downloads Organizer

A simple Python automation tool that sorts the files in a folder (your Downloads by default) into sub-folders by file type. Anything with an unknown extension goes to **Miscellaneous**.

**Author:** Aahish ([@silverbullet-ai](https://github.com/silverbullet-ai))
**Version:** 1.0.0  
**License:** MIT

---

## Features

- Organizes files by extension
- Unknown file types go to `Miscellaneous`
- Never intentionally overwrites existing files (adds `_1`, `_2`, etc. on name conflicts)
- Safe `--dry-run` mode to preview changes
- Logs all operations and errors
- Works on any folder via `--folder`
- Python standard library only, no third-party dependencies

## Requirements

- Python 3.9 or newer

## Project Structure

```text
smart-download-organizer/
├── organizer.py        # main script
├── config.py           # categories, extensions, log location
├── requirements.txt    # empty (standard library only)
├── README.md
├── .gitignore
└── logs/
    └── .gitkeep        # keeps the folder in Git; log file is created on first run
```

## Usage

Preview first (nothing is moved):

```bash
python organizer.py --dry-run
```

Organize your Downloads folder:

```bash
python organizer.py
```

Organize a custom folder:

```bash
python organizer.py --folder "D:\TestDownloads"
```

### Options

| Option            | Description                          | Default         |
| ----------------- | ------------------------------------ | --------------- |
| `--folder PATH` | Folder to organize                   | `~/Downloads` |
| `--dry-run`     | Preview changes without moving files | off             |

## Example

Before:

```text
Downloads/
├── resume.pdf
├── photo.png
├── song.mp3
├── dataset.csv
├── setup.exe
└── mystery.xyz
```

After:

```text
Downloads/
├── Documents/resume.pdf
├── Images/photo.png
├── Music/song.mp3
├── Spreadsheets/dataset.csv
├── Applications/setup.exe
└── Miscellaneous/mystery.xyz
```

## How It Works

1. Reads the extension of each file in the target folder.
2. Known extension: moves it to the matching category folder.
3. Unknown extension: moves it to `Miscellaneous`.
4. If a file with the same name already exists in the destination, the new file is renamed (`report.pdf` becomes `report_1.pdf`).

Only files directly inside the target folder are processed. Existing sub-folders and their contents are left untouched.

## Configuration

Edit `config.py` to add categories or extensions:

```python
CATEGORIES = {
    "Ebooks": [".epub", ".mobi"],   # new category
    ...
}
```

Extensions should be lowercase and include the leading dot.

## Logging

All moves and errors are written to `logs/organizer.log`, next to the scripts.

## Safety Principles

1. Preview with `--dry-run` first.
2. Unknown files go to `Miscellaneous` rather than being skipped or deleted.
3. Existing files are never intentionally overwritten.
4. A failed move does not stop the rest of the run.
5. Every operation is logged.
6. No third-party dependencies.

## License

Released under the MIT License.
