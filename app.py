import streamlit as st
import pandas as pd
from langchain import OpenAI, PromptTemplate, LLMChain
import ast

import os
os.environ["OPENAI_API_KEY"] = "ENTER API KEY HERE"


def load_data(file):
    # Load data from the uploaded file
    try:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.name.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file)
        else:
            st.error('Unsupported file format')
            return None
    except Exception as e:
        st.error(f'Error loading data: {e}')
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
    try:
        data_description = df.describe().to_string()
        quality_insights = chain.run(data_description)
    except Exception as e:
        st.error(f'Error generating data quality insights: {e}')
        quality_insights = None

    return quality_insights

def validate_and_execute_code(code, df):
    try:
        # Validate the code for syntax errors
        ast.parse(code)
    except SyntaxError as e:
        st.error(f"Syntax Error in the generated code: {e}")
        return

    # Create a local namespace for safe execution
    local_namespace = {"pd": pd, "df": df}

    try:
        # Execute the code in a safe environment
        exec(code, {}, local_namespace)
        st.write('Cleaned and preprocessed data preview:')
        st.write(local_namespace['df'].head())
    except Exception as e:
        st.error(f'Error executing code: {e}')

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
            if quality_insights:
                st.write('Data Quality Insights:')
                st.write(quality_insights)
            else:
                st.warning('No data quality insights available.')

            # Get user feedback
            user_feedback = st.text_area('Enter your feedback or additional instructions for data cleaning and preprocessing:')

            # Add a button to generate code
            if st.button('Generate Code'):
                # Use OpenAI and LangChain to generate code for data cleaning and preprocessing
                llm = OpenAI(temperature=0.7)
                code_prompt = PromptTemplate(
                    input_variables=["data_description", "user_feedback"],
                    template="Based on the following data description and user feedback, generate Python code for cleaning and preprocessing the data: \n\nData Description: {data_description}\n\nUser Feedback: {user_feedback}"
                )
                chain = LLMChain(llm=llm, prompt=code_prompt)
                try:
                    code_output = chain.run(data_description=data_description, user_feedback=user_feedback)
                except Exception as e:
                    st.error(f'Error generating code: {e}')
                    return

                st.code(code_output, language='python')

                # Add a run button
                if st.button('Run Code'):
                    validate_and_execute_code(code_output, df)

if __name__ == '__main__':
    main()