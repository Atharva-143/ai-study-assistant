# AI Study Assistant

**AI Study Assistant** is a web application that helps students analyze study materials using Artificial Intelligence and Natural Language Processing (NLP).

The system allows users to upload PDF notes and automatically generate **summaries, quiz questions, keywords, and answers to questions** from the uploaded content.

---

## Features

- Upload and manage **PDF notes**
- Generate **AI-based summaries**
- Ask questions from uploaded notes
- Automatically generate **quiz questions**
- Extract **important keywords**
- Download generated **summary as a PDF**
- Support for **multiple PDFs in a knowledge base**
- Clean and responsive **user interface**
- **Dark mode toggle**

---

## Technologies Used

- Python  
- Flask  
- Hugging Face Transformers  
- PyPDF2  
- RAKE-NLTK  
- NLTK  
- FPDF  
- HTML  
- CSS  
- JavaScript  

---

## Project Structure

```
AI-Study-Assistant
│
├── app.py
├── requirements.txt
├── README.md
│
├── templates
│ └── index.html
│
├── static
│ ├── css
│ │ └── style.css
│ └── js
│ └── script.js
│
└── uploads
```

---

## Installation

### 1. Clone the repository

```
git clone https://github.com/yourusername/ai-study-assistant.git
```

### 2. Navigate to the project folder

```
cd ai-study-assistant
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Run the application

```
python app.py
```

### 5. Open in browser

```
http://127.0.0.1:5000
```

---

## Application Workflow

```
Upload PDF
↓
Extract Text
↓
Clean Text
↓
Generate AI Summary
↓
Generate Quiz Questions
↓
Extract Keywords
↓
Answer Questions from Notes
```

---

## Author

Atharva Besikrao
