
import os
from io import BytesIO

import nltk

# Use the NLTK datasets bundled with this project.
NLTK_DATA_PATH = os.path.join(
    os.path.dirname(__file__),
    "nltk_data"
)

nltk.data.path.insert(0, NLTK_DATA_PATH)

from textblob import TextBlob

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from wordcloud import WordCloud

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.probability import FreqDist


def text_summarize(text, num_sentences=3):
    sentences = sent_tokenize(text)
    words = word_tokenize(text.lower())

    stop_words = set(stopwords.words("english"))
    words = [
        word for word in words
        if word.isalnum() and word not in stop_words
    ]

    frequency_dist = FreqDist(words)
    max_freq = max(frequency_dist.values()) if frequency_dist else 1

    sentence_scores = {}

    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word in frequency_dist:
                if sentence in sentence_scores:
                    sentence_scores[sentence] += (
                        frequency_dist[word] / max_freq
                    )
                else:
                    sentence_scores[sentence] = (
                        frequency_dist[word] / max_freq
                    )

    summary_sentences = sorted(
        sentence_scores,
        key=sentence_scores.get,
        reverse=True
    )[:num_sentences]

    summary = TreebankWordDetokenizer().detokenize(
        summary_sentences
    )

    return summary


def sentiment_analysis(text):
    analysis = TextBlob(text)
    vader = SentimentIntensityAnalyzer()

    vader_scores = vader.polarity_scores(text)

    if analysis.sentiment.polarity > 0:
        result = "Positive"
    elif analysis.sentiment.polarity < 0:
        result = "Negative"
    else:
        result = "Neutral"

    return f"{result} : {vader_scores}"


def word_cloud(text):
    if not text or not text.strip():
        raise ValueError("Input text cannot be empty.")

    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color="white"
    ).generate(text)

    image_buffer = BytesIO()
    figure, axis = plt.subplots(figsize=(10, 5))

    try:
        axis.imshow(wordcloud, interpolation="bilinear")
        axis.axis("off")
        axis.set_title("Word Cloud")

        figure.savefig(
            image_buffer,
            format="png",
            bbox_inches="tight",
            dpi=100
        )

        image_buffer.seek(0)

    finally:
        plt.close(figure)

    return image_buffer
