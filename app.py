import streamlit as st
import pandas as pd
from langchain import OpenAI, PromptTemplate, LLMChain

import os
os.environ["OPENAI_API_KEY"] = "API KEY HERE"


def load_data(file):
    # Load data from the uploaded file
    if file.name.endswith('.csv'):
        df = pd.read_csv(file)
    elif file.name.endswith(('.xls', '.xlsx')):
        df = pd.read_excel(file)
    else:
        st.error('Unsupported file format')
        return None
    return df

def check_data_quality(df):
    # Set up the OpenAI LLM
    llm = OpenAI(temperature=0.7)

    # Define the prompt template
    prompt = PromptTemplate(
        input_variables=["data_description"],
        template="Analyze the following data description and identify any potential data quality issues, such as missing values, outliers, or inconsistent data formats. Provide recommendations for cleaning and preprocessing the data: \n\n{data_description}"
    )

    # Create the LLM chain
    chain = LLMChain(llm=llm, prompt=prompt)

    # Generate data quality insights
    data_description = df.describe().to_string()
    quality_insights = chain.run(data_description)

    return quality_insights

def main():
    st.title('AI-Powered Data Cleaning and Preprocessing Tool')
    file = st.file_uploader('Upload your data file', type=['csv', 'xls', 'xlsx'])

    if file is not None:
        df = load_data(file)
        if df is not None:
            st.write('Data Preview:')
            st.write(df.head())

            # Calculate data description
            data_description = df.describe().to_string()

            # Check data quality
            quality_insights = check_data_quality(df)
            st.write('Data Quality Insights:')
            st.write(quality_insights)

            # Get user feedback
            user_feedback = st.text_area('Enter your feedback or additional instructions for data cleaning and preprocessing:')

            if user_feedback:
                # Use OpenAI and LangChain to generate code for data cleaning and preprocessing
                llm = OpenAI(temperature=0.7)
                code_prompt = PromptTemplate(
                    input_variables=["data_description", "user_feedback"],
                    template="Based on the following data description and user feedback, generate Python code for cleaning and preprocessing the data: \n\nData Description: {data_description}\n\nUser Feedback: {user_feedback}"
                )
                chain = LLMChain(llm=llm, prompt=code_prompt)
                code_output = chain.run(data_description=data_description, user_feedback=user_feedback)

                st.code(code_output, language='python')

                # Execute the generated code
                exec(code_output)

                st.write('Cleaned and preprocessed data preview:')
                st.write(df.head())

if __name__ == '__main__':
    main()