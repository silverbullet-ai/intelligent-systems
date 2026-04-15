![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-Web_App-green)
![NLP](https://img.shields.io/badge/NLP-Text_Analysis-orange)
![GitHub release](https://img.shields.io/github/v/release/silverbullet-ai/intelligent-systems/tree/main/ml/nlp-nexus)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# NLP Nexus  

NLP Nexus is a **Natural Language Processing (NLP) web application** designed to simplify text analysis and document understanding.  
It allows users to summarize large text documents, perform sentiment analysis, and visualize text data using word clouds.

The application provides a simple web interface where users can paste text or upload PDF documents and instantly analyze the content.

---

## Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Running the Application](#️-running-the-application)
- [Project Structure](#-project-structure)
- [Future Improvements](#-future-improvements)
- [Author](#-author)
- [Python Version](#-python-version)
- [License](#-license)

---

## Features

### Text Summarization
Generate concise summaries from long documents by extracting the most important sentences.

### Sentiment Analysis
Analyze text to determine its emotional tone:
- Positive
- Negative
- Neutral

### Word Cloud Generation
Visualize frequently occurring words in the text to quickly understand key themes.

### PDF Text Extraction
Upload PDF documents and extract text automatically for further analysis.

### Web Interface
A simple and interactive UI built with **Flask** for easy text analysis.

---

## Tech Stack

### Backend
- Python
- Flask

### NLP Libraries
- NLTK
- TextBlob

### Visualization
- WordCloud
- Matplotlib

### Utilities
- NumPy
- PyPDF2

---

## Installation

### 1️. Clone the repository

```bash
git clone https://github.com/silverbullet-ai/NLP_Nexus.git
cd NLP_Nexus
```

---

### 2️. Create a virtual environment (recommended)

```bash
python -m venv venv
```

or

```bash
py -3.11 -m venv venv
```

---

### 3️. Activate the virtual environment

**Windows (PowerShell / Command Prompt / Windows Terminal)**

```bash
venv\Scripts\activate
```

**Git Bash**

```bash
source venv/Scripts/activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

---

### 4️. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 5️. Download required NLTK resources

```bash
python -m nltk.downloader punkt
python -m nltk.downloader stopwords
python -m nltk.downloader vader_lexicon
```

---

## Running the Application

Start the Flask server:

```bash
python src/app.py
```

Then open your browser and go to:

```
http://127.0.0.1:5000
```

---

## Project Structure

```
NLP_Nexus
│
├── src                         # Application source code
│   ├── app.py                  # Flask application
│   ├── summarizer.py           # NLP processing logic
│   ├── pdf_extractor.py        # PDF text extraction
│   │
│   ├── templates               # HTML templates
│   │   ├── index.html
│   │   ├── result.html
│   │   └── result1.html
│   │
│   └── static
│       ├── css
│       │   └── style.css
│       │
│       └── images
│           ├── bg.jpg
│           └── icons.jpg
│
├── .gitignore                  # Git ignored files
├── LICENSE                     # MIT License
├── requirements.txt
└── README.md
```

---

## Future Improvements

- Download generated word clouds
- Copy summary button
- Improved NLP models
- Additional visualizations
- Enhanced UI/UX

---

## Author

**silverbullet-ai (Aahish)**  

GitHub: https://github.com/silverbullet-ai

---

## Python Version

This project was developed and tested using:

**Python 3.11**

Using Python 3.11 is recommended for compatibility with the dependencies.

---

## License

This project is licensed under the **MIT License**.  

See the [LICENSE](LICENSE) file for details.

---

⭐ If you like this project, consider giving it a **star on GitHub!**
