from flask import Flask, render_template, request
from summarizer import text_summarize, sentiment_analysis, word_cloud
from pdf_extractor import extract_text_from_pdf

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    text = request.form.get("text", "")
    action = request.form.get("action")
    pdf_file = request.files.get("pdf_file")

    # Extract text from PDF if uploaded
    if pdf_file and pdf_file.filename != "":
        pdf_text = extract_text_from_pdf(pdf_file)
        text += "\n" + pdf_text

    # Handle empty input
    if not text.strip():
        return render_template(
            "summary.html",
            result="No text provided."
        )

    # Summarization
    if action == "summarize":
        result = text_summarize(text)
        return render_template("summary.html", result=result)

    elif action == "sentiment":
        result = sentiment_analysis(text)

        print("Sentiment Output:", result)

        result_str = str(result).lower()
        compound = 0

        if "compound" in result_str:
            try:
                compound = float(result_str.split("compound':")[1].split("}")[0])
            except:
                compound = 0

        # Classification using compound score
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
            details=result  
        )

    # Word Cloud
    elif action == "wordcloud":
        filename = "wordcloud.png"
        word_cloud(text, filename)
        return render_template("wordcloud.html")

    # Fallback
    return render_template(
        "summary.html",
        result="Invalid request."
    )


if __name__ == "__main__":
    app.run(debug=True)