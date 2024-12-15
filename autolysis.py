"""import subprocess
import sys

# List of required libraries
required_libraries = [
    'pandas',
    'dotenv',
    'openai',
    'chardet',
    'scikit-learn',
    'matplotlib',
    'requests',
    'seaborn'
]"""

"""def install_libraries(libraries):
     """#Check and install the required libraries if not already installed."""
    """for library in libraries:
        try:
            __import__(library)  # Try to import the library
        except ImportError:
            print(f"Library '{library}' not found. Installing...")
            subprocess.check_call(["uv", "add", library])

# Install the required libraries at runtime
install_libraries(required_libraries)

import sys
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os
import requests
import json
import chardet
from sklearn.preprocessing import LabelEncoder

def detect_file_encoding(file_path):
    """Detect the encoding of the input file."""
    with open(file_path, "rb") as file:
        result = chardet.detect(file.read())
    return result['encoding']

def load_dataset(file_path, encoding):
    """Load the dataset with the given encoding."""
    return pd.read_csv(file_path, encoding=encoding)

def initialize_api_details():
    """Initialize API details from environment variables."""
    load_dotenv()
    return {
        "token": os.getenv("IITM_API_KEY"),
        "base_url": "https://aiproxy.sanand.workers.dev/openai/v1",
    }

def prepare_null_handling_prompt(dataset):
    """Prepare the prompt to handle null values based on dataset information."""
    null_values = {
        col: float(dataset[col].isna().sum()) / dataset.shape[0] for col in dataset.columns
    }
    return f"""
    You are a Python Data Analyst.
    Name of the Dataset = "dataset".
    You do not read the data from a path, assume that the data is present in a variable called "dataset".
    You are given a "dataset" with the following columns and their respective percentage of null values: {null_values}.
    Based on this information, decide whether to delete the entire column, drop rows containing nulls, or impute values logically.
    Before you impute or delete, always check whether the column exists.
    The "dataset" should remain as a pandas DataFrame.
    Import necessary libraries.
    Your output should be only code with no explanations, justifications, or comments whatsoever.
    """

def prepare_feature_relevance_prompt(dataset):
    encoder = LabelEncoder()
    encodedDataset = dataset.copy(deep=True)
    for col in encodedDataset.columns:
        if encodedDataset[col].dtype == "object":
            encodedDataset[col] = encoder.fit_transform(encodedDataset[col])
    correlation_matrix = encodedDataset.corr()
    columns = [col for col in dataset.columns]
    datatypes = [dataset[col].dtype for col in dataset.columns]
    summary = dataset.describe()

    prompt = f"""
You are an expert in data analysis.
Assume the dataset is called dataset.

The following information is provided:

Correlation Matrix: {correlation_matrix}
Column Names: {columns}
Original Data Types: {datatypes}
Basic Summary: {summary}

Your task is to:

Make an educated guess about the target variable based on logical reasoning.
Remove irrelevant features only if the number of features is more than 10.
Remove features by analyzing the correlation, data types, and uniqueness of each column.
Use the correlation matrix and summary given to you.
Drop features with high missingness, low correlation, or high uniqueness (like IDs).
The output must be only Python code, with no comments or explanations.
Do not output anything other than the code.
Ensure the code cleanly removes the irrelevant features from the DataFrame named "dataset".
The new dataset is also stored as "dataset".
"""
    return prompt


def call_openai_api(api_details, endpoint, prompt, functions=None):
    """Make a request to the OpenAI API and return the response."""
    url = f"{api_details['base_url']}/{endpoint}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_details['token']}"
    }
    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
    }
    if functions:
        data["functions"] = functions
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API Error: {response.status_code}, {response.text}")

def execute_code(code):
    """Execute the Python code returned by the API."""
    
    try:
        exec(code, globals())
        print("Code Executed Successfully")
    except Exception as e:
        print("Error during code execution:", e)

def write_into_file(content):

    with open("README.md", "w") as file:
        file.write(content)

def handle_null_values(dataset, api_details):
    """Generate and execute code to handle null values in the dataset."""
    prompt = prepare_null_handling_prompt(dataset)
    response = call_openai_api(api_details, "chat/completions", prompt)
    code = response['choices'][0]['message']['content']
    clean_code = code.strip("```").strip("python").strip()
    print(clean_code)
    execute_code(clean_code)

def feature_relevance(dataset, api_details):

    prompt = prepare_feature_relevance_prompt(dataset)
    response = call_openai_api(api_details, "chat/completions", prompt)
    code = response['choices'][0]['message']['content']
    clean_code = code.strip("```").strip("python").strip()
    print(clean_code)
    execute_code(clean_code)


def generate_boxplots(columns, dataset):
    """Generate box plots for the specified columns to detect outliers."""
    plt.figure(figsize=(10, 6))
    dataset[columns].boxplot()
    plt.title('Box Plots for Outlier Detection')
    plt.show()

def remove_outliers(dataset, columns):
    """Remove outliers from the dataset based on the IQR method."""
    cleaned_data = dataset.copy()
    for column in columns:
        Q1 = cleaned_data[column].quantile(0.25)
        Q3 = cleaned_data[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        cleaned_data = cleaned_data[(cleaned_data[column] >= lower_bound) & (cleaned_data[column] <= upper_bound)]
    return cleaned_data

def handle_outliers(dataset, columns, api_details):
    """Generate box plots, remove outliers, and return the cleaned dataset."""
    functions = [
        {
            "name": "generate_boxplots",
            "description": "Generate box plots for outlier detection.",
            "parameters": {
                "type": "object",
                "properties": {
                    "columns": {"type": "array", "items": {"type": "string"}},
                    "dataset": {"type": "object"}
                }
            }
        },
        {
            "name": "remove_outliers",
            "description": "Remove outliers from the dataset.",
            "parameters": {
                "type": "object",
                "properties": {
                    "dataset": {"type": "object"},
                    "columns": {"type": "array", "items": {"type": "string"}}
                }
            }
        }
    ]

    prompt = f"""
    Name of the dataset = "dataset"
    I have a dataset with the following numerical columns: {', '.join(columns)}.
    Perform the following tasks:
    1. Generate box plots to visualize potential outliers.
    2. Remove identified outliers based on your analysis.
    """
    response = call_openai_api(api_details, "chat/completions", prompt, functions)
    cleaned_data = remove_outliers(dataset, columns)
    return cleaned_data

def visualize_data(dataset, columns, datatypes, api_details):
    """Generate visualizations for the dataset using Seaborn and Matplotlib."""
    prompt = f"""
    You are a Python Data Analyst.
    Given the following column names: {columns}
    And their respective datatypes: {datatypes}
    Assume that the dataset is already imported.
    *IMPORTANT* Name of the dataset: "dataset"

    Generate Python code using Seaborn to:
    1. Calculate the correlation between columns (convert categorical to numerical if needed).
    2. Convert any date column into datetime using "to_datetime" method in pandas.
    3. Generate a maximum of 3 visualizations, including a correlation heatmap. Do not use "Country Names".
    4. Generate plots mainly for highly correlated fields.
    Exclude pairplots and focus on concise, meaningful plots.
    Export plots in PNG format as '1.png', '2.png', etc.
    Make sure there is only 1 plot per Image.
    The Image must be clear.
    Output only the Python code.
    """
    response = call_openai_api(api_details, "chat/completions", prompt)
    code = response['choices'][0]['message']['content']
    clean_code = code.strip("```").strip("python").strip()
    print(clean_code)
    execute_code(clean_code)

def narrate_data(dataset, columns, datatypes, api_details):

    summary = dataset.describe()
    prompt = f"""
Create a README.md file for my data analysis project.
Name of the columns = {columns}
Datatype of columns = {datatypes}
Summary of dataset = {summary}

The README must include the following sections:
1. About the Data: Briefly describe the data, its source, key attributes, and unique characteristics.
2. Analysis Performed: List and describe the key analysis techniques, methods, and statistical approaches used.
3. Insights Discovered: Highlight the main takeaways, trends, and patterns revealed from the analysis.
4. Implications & Recommendations: Based on the insights, suggest actions, recommendations, or next steps.

Additionally, incorporate the following three image files as part of the README:

1.png: Include this image in the "Analysis Performed" section to visualize key analysis steps.
2.png: Place this image in the "Insights Discovered" section to illustrate key trends.
3.png: Place this image in the "Implications & Recommendations" section to support the conclusions.
Use proper Markdown syntax, including headers (##), bullet points, and image tags like ![Alt text](path/to/image.png).
The README should be clear, professional, and concise, following best practices for open-source documentation.
Do not include any explanations, justifications, or comments. Only output the Markdown file.
"""
    response = call_openai_api(api_details, "chat/completions", prompt)
    code = response['choices'][0]['message']['content']
    clean_code = code.strip("```").strip("markdown").strip()
    write_into_file(clean_code)

def main():
    """Main function to handle dataset processing."""
    dataset_file = sys.argv[1]
    encoding = detect_file_encoding(dataset_file)
    global dataset 
    dataset = load_dataset(dataset_file, encoding)
    api_details = initialize_api_details()
    # Handle null values
    handle_null_values(dataset, api_details)
    # Feature Relevance
    if dataset.shape[1] > 10:
        feature_relevance(dataset, api_details)
    # Handle outliers
    numerical_columns = [col for col in dataset.select_dtypes(include=['float64', 'int64']).columns]
    cleaned_data = handle_outliers(dataset, numerical_columns, api_details)
    # Visualize data
    columns = dataset.columns.tolist()
    datatypes = dataset.dtypes.tolist()
    visualize_data(cleaned_data, columns, datatypes, api_details)
    narrate_data(cleaned_data, columns, datatypes, api_details)

if __name__ == "__main__":
    main()
"""
