from flask import Flask, render_template, request, send_from_directory
import os
import PyPDF2
from transformers import pipeline
from rake_nltk import Rake
import nltk
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
from fpdf import FPDF

knowledge_base = ""
summary_storage = ""
app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

summarizer = pipeline("summarization")

@app.route("/")
def home():
    files = os.listdir(app.config["UPLOAD_FOLDER"])
    return render_template("index.html", files=files)


@app.route("/upload", methods=["POST"])
def upload_file():

    file = request.files["file"]

    if file:

        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        summary = ""

        if file.filename.endswith(".pdf"):

            text = extract_text_from_pdf(filepath)
            global knowledge_base
            knowledge_base += " " + text

            print("\n----- PDF TEXT START -----\n")
            print(text[:1000])
            print("\n----- PDF TEXT END -----\n")

            summary = generate_summary(text)
            global summary_storage
            summary_storage = summary

        return render_template(
            "index.html",
            filename=file.filename,
            files=os.listdir(app.config["UPLOAD_FOLDER"]),
            summary=summary
        )

    return render_template(
        "index.html",
        files=os.listdir(app.config["UPLOAD_FOLDER"])
    )


@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/delete/<filename>")
def delete_file(filename):

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    if os.path.exists(file_path):
        os.remove(file_path)

    files = os.listdir(app.config["UPLOAD_FOLDER"])

    return render_template("index.html", files=files)


@app.route("/preview/<filename>")
def preview_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/ask", methods=["POST"])
def ask_question():

    question = request.form["question"]

    answer = answer_question(question)

    return render_template(
        "index.html",
        files=os.listdir(app.config["UPLOAD_FOLDER"]),
        answer=answer
    )

@app.route("/quiz")
def quiz():

    questions = generate_quiz(knowledge_base)

    return render_template(
        "index.html",
        files=os.listdir(app.config["UPLOAD_FOLDER"]),
        quiz=questions
    )

@app.route("/keywords")
def keywords():

    keywords = extract_keywords(knowledge_base)

    return render_template(
        "index.html",
        files=os.listdir(app.config["UPLOAD_FOLDER"]),
        keywords=keywords
    )

@app.route("/download_summary")
def download_summary():

    global summary_storage

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font("Arial", size=12)

    for line in summary_storage.split(". "):
        pdf.multi_cell(0, 8, line)

    file_path = "summary.pdf"

    pdf.output(file_path)

    return send_from_directory(".", file_path, as_attachment=True)

def extract_text_from_pdf(filepath):

    text = ""

    with open(filepath, "rb") as file:

        reader = PyPDF2.PdfReader(file)

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text

                text = text.replace("1 of 4", "")
                text = text.replace("2 of 4", "")
                text = text.replace("3 of 4", "")
                text = text.replace("4 of 4", "")
    text = text.replace("\n", " ")
    return text


def generate_summary(text):
    remove_words = [
        "activity",
        "answer key",
        "exercise",
        "practice questions",
        "references",
        "bibliography",
        "table of contents",
        "index"
    ]

    text = text.lower()

    for word in remove_words:
        text = text.replace(word, "")

    text = text.replace("\n", " ")

    text = " ".join(text.split())

    chunk_size = 1500
    summaries = []

    for i in range(0, len(text), chunk_size):

        chunk = text[i:i + chunk_size]

        result = summarizer(
            chunk,
            max_length=80,
            min_length=25,
            do_sample=False
        )

        summaries.append(result[0]["summary_text"])

    final_summary = " ".join(summaries)

    return final_summary

import re

def generate_quiz(text):

    questions = []

    text = text.replace("\n", " ")
    text = " ".join(text.split())

    sentences = re.split(r'[.!?]', text)

    for sentence in sentences:

        sentence = sentence.strip()

        if len(sentence.split()) < 8:
            continue

        if "http" in sentence or "www" in sentence:
            continue

        if re.search(r'\d', sentence):
            continue

        if "(" in sentence or ")" in sentence:
            continue

        question = "Explain: " + sentence + "?"
        questions.append(question)

        if len(questions) == 5:
            break

    return questions

def answer_question(question):

    global pdf_text_storage

    text = knowledge_base.lower()
    question = question.lower()

    text = text.replace("\n", " ")

    sentences = text.split(". ")

    best_match = ""
    best_score = 0

    for sentence in sentences:

        score = sum(word in sentence for word in question.split())

        if score > best_score:
            best_score = score
            best_match = sentence.strip()

    if best_match:
        return best_match

    return "Sorry, I couldn't find a clear answer in the document."

import re
from rake_nltk import Rake

def extract_keywords(text):

    text = re.sub(r'<.*?>', ' ', text)

    text = re.sub(r'[^a-zA-Z\s]', ' ', text)

    text = text.lower()

    text = " ".join(text.split())

    r = Rake()

    r.extract_keywords_from_text(text)

    keywords = r.get_ranked_phrases()

    clean_keywords = []

    for k in keywords:

        words = k.split()
        if len(set(words)) == 1:
            continue

        if len(words) < 2:
            continue

        clean_keywords.append(k)

        if len(clean_keywords) == 10:
            break

    return clean_keywords

if __name__ == "__main__":
    app.run(debug=True)