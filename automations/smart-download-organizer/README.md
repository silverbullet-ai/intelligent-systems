# Smart Download Organizer

A Python-based desktop application that helps organize files automatically by categorizing them into folders based on their file extensions.

Smart Download Organizer provides a graphical interface for scanning directories, previewing organization plans, managing categorization rules, moving files, and undoing previous operations.

## ✨ Features

### File Scanning

- Scan selected directories for files.
- Support for recursive and non-recursive scanning.
- Collect file metadata, including name, extension, size, and modification time.
- Display scan summaries and file statistics.
- Automatically exclude configured organizer category folders during recursive scans.

### Automatic File Categorization

- Categorize files based on their extensions.
- Support for predefined categories.
- Handle unknown file extensions using a configurable default category.
- Case-insensitive extension matching.
- Manage custom categories and file extensions through the GUI.

### Organization Preview

- Preview the proposed organization plan before moving files.
- Review destination folders and file categories.
- Identify potential changes before executing operations.

### File Organization

- Automatically move files into their respective category folders.
- Prevent accidental overwriting of existing files.
- Handle duplicate filenames by generating unique filenames.
- Detect files that have been modified or deleted after scanning.

### Undo Functionality

- Reverse previously completed organization operations.
- Restore files to their original locations.
- Prevent overwriting files during restoration.
- Retain unsuccessful restoration records for future recovery attempts.

### Activity History

- Maintain persistent movement history.
- Record successful file movements.
- Access previous organization activities.

### Configuration Management

- Add and remove custom categories.
- Add and remove file extensions.
- Change the default category.
- Reset categorization rules to their defaults.
- Store configuration rules in JSON format.

### Unit Testing

- Automated tests using Python's `unittest` framework.
- Tests covering scanning, categorization, configuration management, and file organization.
- Validation of duplicate handling, undo operations, and file-change detection.

**Current test status: 45 tests passing.**

---

## Tech Stack

| Technology    | Purpose                              |
| ------------- | ------------------------------------ |
| Python        | Core application logic               |
| CustomTkinter | Graphical user interface             |
| JSON          | Configuration and persistent history |
| pathlib       | File and directory handling          |
| os            | Directory traversal                  |
| shutil        | File movement                        |
| logging       | Application logging                  |
| unittest      | Automated testing                    |

---

## 📁 Project Structure

```text
smart-download-organizer/
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── gui.py
│   ├── scanner.py
│   ├── categorizer.py
│   ├── organizer.py
│   ├── config_manager.py
│   └── logger.py
│
├── config/
│   └── rules.json
│
├── assets/
│   └── icons/
│
├── logs/
│
├── tests/
│   ├── __init__.py
│   ├── test_scanner.py
│   ├── test_categorizer.py
│   ├── test_organizer.py
│   └── test_config_manager.py
│
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/silverbullet-ai/intelligent-systems/tree/main/automations/smart-download-organizer
```

### 2. Navigate to the project directory

```bash
cd smart-download-organizer
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows:**

```powershell
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
python -m src.main
```

---

## Usage

1. Launch Smart Download Organizer.
2. Select the directory you want to organize.
3. Choose whether to scan subdirectories recursively.
4. Start the scanning process.
5. Review the detected files and their assigned categories.
6. Preview the proposed organization plan.
7. Execute the organization operation.
8. Access activity history or undo previous operations when needed.

You can also manage categories and file extensions through the configuration interface.

---

## Running Tests

The project uses Python's built-in `unittest` framework.

Run the complete test suite from the project root:

```bash
python -m unittest discover -s tests -v
```

Run individual test modules:

```bash
python -m unittest tests.test_scanner -v
python -m unittest tests.test_categorizer -v
python -m unittest tests.test_organizer -v
python -m unittest tests.test_config_manager -v
```

### Current Test Coverage

| Module          |        Tests |
| --------------- | -----------: |
| Scanner         |           11 |
| Categorizer     |           12 |
| Config Manager  |           10 |
| Organizer       |           12 |
| **Total** | **45** |

---

## Safety Considerations

Smart Download Organizer includes safeguards to reduce accidental file loss:

- Existing destination files are not overwritten.
- Duplicate filenames receive unique names.
- Files modified after scanning are skipped.
- Deleted files are detected before movement.
- Undo operations check whether the original destination is already occupied.
- File movement history is maintained for reversal.

**Important:** Although safeguards and undo functionality are implemented, always maintain backups of important files. Undo history is not a substitute for a backup system.

---

## 🛣️ Future Improvements

Potential enhancements for future versions:

- [ ] Improved dashboard with file statistics and visualizations.
- [ ] Drag-and-drop folder selection.
- [ ] Scheduled automatic organization.
- [ ] Advanced filtering and search.
- [ ] Additional file metadata and categorization rules.
- [ ] Application packaging into a standalone Windows executable.
- [ ] Improved error reporting and recovery.
- [ ] Dark and light theme customization.

---

## Project Status

<kbd>Active Development</kbd>

The core application functionality has been implemented, and the current test suite passes all 45 tests.

Further improvements will focus on usability, reliability, application packaging, and additional automation capabilities.

---

## 👨‍💻 Author

**SilverBullet AI** 

GitHub: [silverbullet-ai](https://github.com/silverbullet-ai)

---

*Built with Python, curiosity, and a little automation magic.*
