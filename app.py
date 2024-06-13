import streamlit as st
import pandas as pd
from mcq_extractor import generate_and_evaluate_mcqs
from io import BytesIO

st.title("MCQ Generator from PDF")
st.write("Upload a PDF file to extract MCQs and generate a CSV file.")

uploaded_file = st.file_uploader("Upload PDF", type="pdf")
number = st.number_input("Number of MCQs", min_value=1, step=1)
subject = st.text_input("Subject")
tone = st.text_input("Tone")

if st.button("Generate Quiz"):
    if uploaded_file and number and subject and tone:
        try:
            mcqs = generate_and_evaluate_mcqs(uploaded_file, number, subject, tone)
            if mcqs:
                df = pd.DataFrame(mcqs)
                st.write("### Generated MCQs")
                st.dataframe(df)  # Display MCQs in a table
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=BytesIO(csv.encode('utf-8')),
                    file_name='mcqs.csv',
                    mime='text/csv'
                )
            else:
                st.error("No MCQs extracted from the PDF.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.error(traceback.format_exc())
    else:
        st.error("Please upload a PDF file and fill all the fields.")