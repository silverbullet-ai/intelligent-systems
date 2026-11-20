# 🧠 NLP Nexus

<p align="center">
  <strong>Understand Text. Discover Meaning.</strong>
  <br>
  A Natural Language Processing web application for exploring, analyzing, and understanding text.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.12">
  <img src="https://img.shields.io/badge/Flask-3.1.3-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/NLP-Text_Analysis-00A6A6?style=for-the-badge" alt="NLP">
  <img src="https://img.shields.io/badge/Deployment-Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white" alt="Vercel">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="MIT License">
</p>

---

## About the Project

**NLP Nexus** is a web-based Natural Language Processing application built with Python and Flask. It brings together essential text analysis capabilities in one interactive interface, helping users extract meaningful information and discover insights from written content.

Whether you want to summarize a lengthy passage, understand its sentiment, or visualize frequently occurring words, NLP Nexus provides a simple way to explore text using NLP techniques.

The application also supports PDF text extraction, allowing users to analyze text directly from PDF documents.

## Key Features

### 📝 Text Summarization

- Generates concise summaries from longer text.
- Identifies important sentences to retain the central meaning.
- Helps reduce lengthy content into more manageable summaries.

### 💬 Sentiment Analysis

- Analyzes the emotional tone of the submitted text.
- Classifies sentiment as Positive, Negative, or Neutral.
- Uses TextBlob and VADER for sentiment analysis.

### ☁️ Word Cloud Generation

- Generates visual representations of frequently occurring words.
- Highlights prominent terms in the submitted content.
- Supports previewing and downloading the generated word cloud.

### 📄 PDF Text Extraction

- Extracts text from uploaded PDF documents.
- Allows extracted content to be used for analysis.
- Handles encrypted PDFs and documents without extractable text.

*Note: Scanned image-only PDFs are not supported because OCR functionality is not currently implemented.*

### 🌐 Interactive Web Interface

- Built with Flask, HTML, CSS, and JavaScript.
- Provides separate interfaces for different analysis operations.
- Includes navigation between the homepage and result pages.
- Preserves text and uploaded PDF selections while navigating within the browser session.

## Installation

Follow these steps to run NLP Nexus locally.

### 1. Clone the Repository

```bash
git clone https://github.com/silverbullet-ai/intelligent-systems/tree/main/ml/nlp-nexus
cd NLP_Nexus
```

### 2. Create a Virtual Environment

**Using Conda:**

```bash
conda create -n nlp-nexus python=3.12 -y
conda activate nlp-nexus
```

**Alternatively, using Python venv:**

```bash
python -m venv .venv
```

Activate the environment:

**Windows:**

```bash
.venv\Scripts\activate
```

**Linux / macOS:**

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

Upgrade pip and install the required packages:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Run the Application

Start the Flask application from the project root:

```bash
python -m src.app
```

Open your browser and visit:

```text
http://127.0.0.1:5000/
```

## Usage

1. Launch NLP Nexus in your browser.
2. Enter text into the input area or upload a PDF document.
3. Choose the desired operation:
   - **Summarization** – Generate a concise version of the submitted text.
   - **Sentiment Analysis** – Identify the sentiment of the text.
   - **Word Cloud** – Generate a visual representation of frequently used words.
4. View the generated results.
5. Copy or download supported results where available.
6. Return to the homepage to perform another analysis.

## Tech Stack

| Technology   | Purpose                                          |
| ------------ | ------------------------------------------------ |
| Python 3.12  | Core programming language                        |
| Flask        | Web application framework                        |
| NLTK         | Tokenization, stopwords, and language processing |
| TextBlob     | Text processing and sentiment analysis           |
| VADER        | Rule-based sentiment analysis                    |
| NumPy        | Numerical operations                             |
| PyPDF2       | PDF text extraction                              |
| Matplotlib   | Visualization support                            |
| WordCloud    | Word cloud generation                            |
| HTML5 & CSS3 | Frontend structure and styling                   |
| JavaScript   | Client-side interactions and input persistence   |
| Vercel       | Planned deployment platform                      |

## Project Structure

```text
NLP_Nexus/
│
├── public/
│   ├── css/
│   │   └── style.css
│   │
│   └── images/
│       ├── bg.jpg
│       └── icons.jpg
│
├── src/
│   ├── __init__.py
│   ├── app.py
│   ├── pdf_extractor.py
│   ├── summarizer.py
│   │
│   ├── nltk_data/
│   │   ├── corpora/
│   │   │   └── stopwords/
│   │   ├── sentiment/
│   │   │   └── vader_lexicon.zip
│   │   └── tokenizers/
│   │       ├── punkt/
│   │       └── punkt_tab/
│   │
│   └── templates/
│       ├── index.html
│       ├── sentiment.html
│       ├── summary.html
│       └── wordcloud.html
│
├── .gitignore
├── .python-version
├── LICENSE
├── requirements.txt
└── README.md
```

## NLTK Resource Management

NLP Nexus uses locally bundled NLTK datasets to ensure the required language-processing resources are available when the application runs.

The following resources are included:

- `punkt` – Sentence and word tokenization support.
- `punkt_tab` – Additional tokenizer data.
- `stopwords` – Common stopwords for text processing.
- `vader_lexicon` – Lexicon required for VADER sentiment analysis.

These resources are stored under `src/nltk_data/`, and the application is configured to use this local directory.

This avoids relying on runtime NLTK downloads when the application starts.

## Deployment

NLP Nexus is being prepared for deployment on **Vercel**.

The deployment setup uses:

- Python 3.12 runtime.
- Dependencies managed through `requirements.txt`.
- Application code organized under `src/`.
- Static assets maintained in the root-level `public/` directory.
- Locally bundled NLTK resources.

Deployment will be completed after the repository is connected to Vercel and the hosted application has been verified.

## Live Project

<p align="center">
  <strong>NLP Nexus — Live Application</strong>
  <br><br>
  <em>Live application link will be added after successful deployment.</em>
</p>

## Future Improvements

- [ ] Add OCR support for scanned PDF documents.
- [ ] Improve summarization algorithms and summary quality.
- [ ] Support additional document formats.
- [ ] Explore more advanced sentiment analysis techniques.
- [ ] Introduce additional text visualization features.
- [ ] Improve application performance and user experience.

## Project Status

<details>
  <summary><strong>Development Progress</strong></summary>

- [X] Flask application setup
- [X] Text summarization
- [X] Sentiment analysis
- [X] Word cloud generation
- [X] PDF text extraction
- [X] Frontend integration
- [X] Input persistence during navigation
- [X] Local NLTK resource configuration
- [X] Python 3.12 compatibility verification
- [X] Local application testing
- [ ] Vercel deployment
- [ ] Live application verification

</details>

## 👨‍💻 Author

**Aahish (Silver Bullet)**

AIML Graduate | Aspiring AI Engineer  

- GitHub: [@silverbullet-ai](https://github.com/silverbullet-ai)

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<p align="center">
  <strong>Built with Python, curiosity, and a passion for language technology.</strong>
  <br>
  <em>Explore Language. Discover Intelligence.</em>
</p>
