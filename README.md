# DDR Report Generator

A Python-based pipeline that reads two PDF files — a building inspection report and a thermal imaging report — and automatically generates a structured Detailed Diagnostic Report (DDR) in `.docx` format.

Built as part of an AI/ML internship assignment.

---

## What it does

- Extracts text and images from both PDFs using PyMuPDF
- Sends the extracted content to Groq's LLaMA 3.3 70B model for analysis
- Gets back a structured JSON with observations, root causes, severity ratings, and recommendations
- Builds a clean Word document with all 7 DDR sections

---

## Stack

- Python 3.13
- PyMuPDF — PDF extraction
- Groq API (LLaMA 3.3 70B) — AI analysis
- python-docx — report generation

---

## Setup

1. Clone the repo
2. Create a virtual environment and install dependencies:
```
   pip install pymupdf python-docx groq python-dotenv
```
3. Create a `.env` file in the root folder:
```
   GROQ_API_KEY=your_key_here
```
4. Place your PDFs in the `input/` folder
5. Run:
```
   python main.py
```
6. Output will be saved to `OUTPUT/DDR_Report.docx`

---

## Project Structure
```
ddr-report-generator/
├── input/                  # Input PDFs
├── OUTPUT/                 # Generated report (auto-created)
├── EXTRACTED_IMAGES/       # Extracted images (auto-created)
├── extract.py              # PDF extraction logic
├── generate.py             # Groq AI integration
├── build_report.py         # Word document builder
├── main.py                 # Entry point
└── .gitignore
```

---

Made by Purojita Singh