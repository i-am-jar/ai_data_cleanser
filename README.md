# AI-Powered Data Cleaning and Preprocessing Tool

This is a Streamlit application that allows users to upload spreadsheet files (CSV, XLS, XLSX) and perform data cleaning and preprocessing with the help of OpenAI's language model. The application analyzes the uploaded data, identifies potential data quality issues, and provides recommendations for cleaning and preprocessing. Users can then provide feedback or additional instructions, and the application will generate and execute Python code to clean and preprocess the data accordingly.

## Features

- File uploader to load spreadsheet data (CSV, XLS, XLSX)
- Data preview and description
- AI-powered data quality analysis using OpenAI's language model
- User feedback input for data cleaning and preprocessing instructions
- Automated generation of Python code for data cleaning and preprocessing
- Validation and safe execution of the generated code
- Display of cleaned and preprocessed data

## Installation

1. Clone the repository or download the source code.
2. Install the required Python packages: pip install streamlit pandas plotly langchain openai
3. Set up your OpenAI API key as an environment variable:
export OPENAI_API_KEY=<your_openai_api_key>


Copy code

## Usage

1. Run the Streamlit application: streamlit run app.py
2. Upload your spreadsheet file using the file uploader in the application.
3. The application will display a preview of the uploaded data and generate a data description.
4. The AI-powered data quality analysis will provide insights and recommendations for cleaning and preprocessing the data.
5. Enter your feedback or additional instructions in the provided text area.
6. The application will generate Python code based on the data description and user feedback.
7. The generated code will be validated for syntax errors and executed in a safe environment.
8. The cleaned and preprocessed data preview will be displayed.

## Contributing

Contributions are welcome! If you find any issues or would like to add new features, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).