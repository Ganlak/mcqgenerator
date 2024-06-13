# MCQ Generator from PDF

This Streamlit application allows users to upload a PDF file, extract multiple-choice questions (MCQs) from the content, and output the extracted MCQs into a CSV file.

## Features
- Upload PDF files.
- Extract text from PDFs.
- Generate MCQs based on the extracted text.
- Download the generated MCQs in a CSV format.

## Directory Structure

mcq_generator/
|-- app.py
|-- mcq_extractor.py
|-- requirements.txt
|-- README.md

## Requirements
- Streamlit
- Pandas
- PyMuPDF
- Langchain
- Python-dotenv

## Installation

1. Clone the repository:
   git clone https://github.com/your-repo/mcq_generator.git

2. Navigate to the project directory:
   cd mcq_generator

3. Install the required packages:
   pip install -r requirements.txt

## Usage

1. Create a `.env` file in the project directory and add your OpenAI API key:
   OPENAI_API_KEY=your_openai_api_key
2. Run the Streamlit app:
   streamlit run app.py
3. Upload a PDF file.
4. Enter the number of MCQs, subject, and tone.
5. Click on "Generate Quiz" to extract MCQs and download the CSV file.