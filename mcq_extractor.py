import fitz  # PyMuPDF
import json
import os
import pandas as pd
import traceback
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.callbacks import get_openai_callback
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(openai_api_key=KEY, model_name="gpt-3.5-turbo", temperature=0.5)

TEMPLATE = """
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to create a quiz of {number} multiple choice questions for {subject} students in {tone} tone. 
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like RESPONSE_JSON below and use it as a guide. 
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}
"""

RESPONSE_JSON = {
    "1": {
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    },
    "2": {
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    }
}

quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template=TEMPLATE
)

TEMPLATE2 = """
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students. 
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
If the quiz is not at par with the cognitive and analytical abilities of the students, 
update the quiz questions which need to be changed and change the tone such that it perfectly fits the student abilities.
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""

quiz_evaluation_prompt = PromptTemplate(
    input_variables=["subject", "quiz"], 
    template=TEMPLATE2
)

quiz_chain = LLMChain(llm=llm, prompt=quiz_generation_prompt, output_key="quiz", verbose=True)
review_chain = LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key="review", verbose=True)

generate_evaluate_chain = SequentialChain(
    chains=[quiz_chain, review_chain], 
    input_variables=["text", "number", "subject", "tone", "response_json"],
    output_variables=["quiz", "review"], 
    verbose=True,
)

def generate_and_evaluate_mcqs(uploaded_file, number, subject, tone):
    try:
        pdf_text = ""
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        for page in doc:
            pdf_text += page.get_text()

        with get_openai_callback() as cb:
            response = generate_evaluate_chain({
                "text": pdf_text,
                "number": number,
                "subject": subject,
                "tone": tone,
                "response_json": json.dumps(RESPONSE_JSON)
            })

        quiz = response.get("quiz")
        
        # Debugging log to check the content of quiz
        print("Quiz JSON content before cleaning:", quiz)
        
        # Remove any extraneous text (e.g., '### RESPONSE_JSON')
        start_index = quiz.find("{")
        if start_index != -1:
            quiz = quiz[start_index:]
        
        # Debugging log to check the content of quiz after cleaning
        print("Quiz JSON content after cleaning:", quiz)

        if not quiz:
            raise ValueError("Quiz content is empty")

        quiz = json.loads(quiz)
        
        quiz_table_data = []
        for key, value in quiz.items():
            mcq = value["mcq"]
            options = " | ".join([f"{option}: {option_value}" for option, option_value in value["options"].items()])
            correct = value["correct"]
            quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})

        return quiz_table_data

    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
        print(traceback.format_exc())
        return []
    except Exception as e:
        print(f"Error: {e}")
        print(traceback.format_exc())
        return []
