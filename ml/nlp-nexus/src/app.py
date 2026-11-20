
import ast
import base64
import os

from flask import Flask, render_template, request

from .summarizer import (
    text_summarize,
    sentiment_analysis,
    word_cloud
)
from .pdf_extractor import extract_text_from_pdf


# --------------------------------------------------
# Flask Application Configuration
# --------------------------------------------------

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="../public",
    static_url_path=""
)


# --------------------------------------------------
# Home Route
# --------------------------------------------------

@app.route("/", methods=["GET", "POST"])
def index():

    # Restore previously submitted text
    text = request.form.get("original_text", "")

    return render_template(
        "index.html",
        text=text
    )


# --------------------------------------------------
# Text Analysis Route
# --------------------------------------------------

@app.route("/analyze", methods=["POST"])
def analyze():

    text = request.form.get("text", "")
    action = request.form.get("action")
    pdf_file = request.files.get("pdf_file")

    # ----------------------------------------------
    # PDF Text Extraction
    # ----------------------------------------------

    if pdf_file and pdf_file.filename != "":

        try:
            pdf_text = extract_text_from_pdf(pdf_file)

            if pdf_text:
                text += "\n" + pdf_text

        except Exception as error:

            print(f"PDF Extraction Error: {error}")

            return render_template(
                "summary.html",
                result="Unable to process the uploaded PDF.",
                original_text=text
            )

    # ----------------------------------------------
    # Input Validation
    # ----------------------------------------------

    if not text.strip():

        return render_template(
            "summary.html",
            result="No text provided.",
            original_text=text
        )

    # ----------------------------------------------
    # Text Summarization
    # ----------------------------------------------

    if action == "summarize":

        result = text_summarize(text)

        return render_template(
            "summary.html",
            result=result,
            original_text=text
        )

    # ----------------------------------------------
    # Sentiment Analysis
    # ----------------------------------------------

    elif action == "sentiment":

        result = sentiment_analysis(text)

        print("Sentiment Output:", result)

        compound = 0.0

        try:

            scores_string = result.split(":", 1)[1].strip()

            scores = ast.literal_eval(scores_string)

            compound = float(scores.get("compound", 0.0))

        except (
            ValueError,
            SyntaxError,
            IndexError,
            AttributeError
        ):

            print("Unable to extract VADER compound score.")

        if compound >= 0.05:

            sentiment_label = "Positive"
            color = "positive"

        elif compound <= -0.05:

            sentiment_label = "Negative"
            color = "negative"

        else:

            sentiment_label = "Neutral"
            color = "neutral"

        return render_template(
            "sentiment.html",
            result=sentiment_label,
            color=color,
            details=result,
            original_text=text
        )

    # ----------------------------------------------
    # WordCloud Generation
    # ----------------------------------------------

    elif action == "wordcloud":

        try:

            image_buffer = word_cloud(text)

            image_data = base64.b64encode(
                image_buffer.getvalue()
            ).decode("utf-8")

            return render_template(
                "wordcloud.html",
                image_data=image_data,
                original_text=text
            )

        except ValueError:

            return render_template(
                "summary.html",
                result=(
                    "Unable to generate a WordCloud. "
                    "Please provide meaningful text."
                ),
                original_text=text
            )

        except Exception as error:

            print(f"WordCloud Generation Error: {error}")

            return render_template(
                "summary.html",
                result=(
                    "Something went wrong while "
                    "generating the WordCloud."
                ),
                original_text=text
            )

    # ----------------------------------------------
    # Invalid Action
    # ----------------------------------------------

    return render_template(
        "summary.html",
        result="Invalid request.",
        original_text=text
    )


# --------------------------------------------------
# Application Entry Point
# --------------------------------------------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=os.environ.get(
            "FLASK_DEBUG", "false"
        ).lower() == "true"
    )
