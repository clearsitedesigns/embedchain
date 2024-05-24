import os
import json
import shutil
import sys
import markdown
import PyPDF2
from embedchain import App
from tqdm import tqdm
from colorama import Fore, Style

# Function to prompt user for input with a default value
def prompt_with_default(prompt, default):
    user_input = input(f"{prompt} (default: {default}): ")
    return user_input.strip() or default

# Function to list existing databases
def list_existing_databases():
    databases = [name for name in os.listdir(".") if os.path.isdir(name)]
    if databases:
        print(Fore.CYAN + "Existing databases:" + Style.RESET_ALL)
        for db in databases:
            print(Fore.CYAN + f"- {db}" + Style.RESET_ALL)
    else:
        print(Fore.YELLOW + "No existing databases found." + Style.RESET_ALL)

# Function to save database creation names in a JSON file
def save_database_names(database_names):
    with open("database_names.json", "w") as f:
        json.dump(database_names, f)

# Load existing database names from JSON file
if os.path.exists("database_names.json"):
    with open("database_names.json", "r") as f:
        existing_database_names = json.load(f)
else:
    existing_database_names = []

# Prompt user for database name
database_name = prompt_with_default("Enter database name", "default_database")

# Check if database name already exists
if database_name in existing_database_names:
    print(Fore.RED + "Database name already exists. Please choose a different name." + Style.RESET_ALL)
    sys.exit(1)

# Prompt user for collection name
collection_name = prompt_with_default("Enter collection name", "default_collection")

# Prompt user for chunking strategy
print(Fore.MAGENTA + "Determine chunking strategy:" + Style.RESET_ALL)
is_text = input("Is the data type text? [yes/no] (default: yes): ").strip().lower() or "yes"
is_text = is_text == "yes"

if is_text:
    strategy_message = "Using default embedding method for text data."
    chunk_size = 300
    chunk_overlap = 50
    min_chunk_size = 200
else:
    fine_grained_analysis = input("Are the analysis objectives fine-grained? (yes/no): ").strip().lower() == "yes"
    high_detail_needed = input("Is high detail needed for analysis? (yes/no): ").strip().lower() == "yes"
    limited_resources = input("Are computational resources limited? (yes/no): ").strip().lower() == "yes"
    domain_specific = input("Are there any domain-specific considerations? (yes/no): ").strip().lower() == "yes"

    if fine_grained_analysis or high_detail_needed:
        strategy_message = "Use smaller chunk sizes with more overlap to capture semantic meaning."
        chunk_size = 200
        chunk_overlap = 100
        min_chunk_size = 100
    else:
        strategy_message = "Use larger chunk sizes with less overlap for broader analysis."
        chunk_size = 400
        chunk_overlap = 50
        min_chunk_size = 200

print(Fore.GREEN + strategy_message + Style.RESET_ALL)

# EmbedChain configuration
config = {
    "llm": {
        "provider": "ollama",
        "config": {
            "base_url": "http://localhost:11434",
            "model": "llama3:latest",
            "temperature": 0.2,
            "top_p": 1,
            "stream": True
        }
    },
    "embedder": {
        "provider": "huggingface",
        "config": {
            "model": "BAAI/bge-small-en-v1.5"
        }
    },
    "vectordb": {
        "provider": "chroma",
        "config": {
            "collection_name": collection_name,
            "dir": database_name,
            "allow_reset": True
        }
    },
    "chunker": {
        "chunk_size": chunk_size,
        "chunk_overlap": chunk_overlap,
        "length_function": "len",
        "min_chunk_size": min_chunk_size
    }
}

# Initialize EmbedChain app
app = App.from_config(config=config)

# List existing databases
list_existing_databases()

# Save database name in the list of existing databases
existing_database_names.append(database_name)
save_database_names(existing_database_names)

# Path to the directory containing various file types
directory_path = input("Please enter the full path to the directory containing files to embed: ")

# Function to read text from various file types, including subdirectories
def read_files_from_directory(directory):
    file_data = []
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            if filename.endswith(".txt"):
                with open(filepath, 'r') as file:
                    text_content = file.read()
                    metadata = {"source": filepath, "document_id": f"doc_{len(file_data)}", "file_name": filename}
                    file_data.append({"text": text_content, "metadata": metadata})
            elif filename.endswith(".md"):
                with open(filepath, 'r') as file:
                    md_content = file.read()
                    html_content = markdown.markdown(md_content)
                    metadata = {"source": filepath, "document_id": f"doc_{len(file_data)}", "file_name": filename}
                    file_data.append({"text": html_content, "metadata": metadata})
            elif filename.endswith(".pdf"):
                with open(filepath, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    pdf_text = ''
                    for page in range(len(reader.pages)):
                        pdf_text += reader.pages[page].extract_text()
                    metadata = {"source": filepath, "document_id": f"doc_{len(file_data)}", "file_name": filename}
                    file_data.append({"text": pdf_text, "metadata": metadata})
    return file_data

# Read text data from directory
file_data = read_files_from_directory(directory_path)

# Embed the data and add it to the collection
num_documents = len(file_data)
for idx, data in enumerate(tqdm(file_data, desc="Embedding Documents")):
    try:
        # Check if document with the same metadata already exists
        if not app.exists(data["metadata"]["document_id"]):
            app.add(data["text"], metadata=data["metadata"])
            print(Fore.GREEN + f"Added document {data['metadata']['document_id']} to collection with source {data['metadata']['source']}." + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + f"Document {data['metadata']['document_id']} already exists in collection. Skipping insertion." + Style.RESET_ALL)
        sys.stdout.flush()
    except AttributeError as e:
        # Database does not exist, proceed with insertion without checking for existence
        app.add(data["text"], metadata=data["metadata"])
        print(Fore.GREEN + f"Added document {data['metadata']['document_id']} to collection with source {data['metadata']['source']}." + Style.RESET_ALL)
        sys.stdout.flush()

# Prompt user to enter the topic area
topic_area = input("Please enter the topic area for analysis: ")

# Define queries for analyzing the top topics
queries = [
    {
        "query": f"""
        Analyze the embedded content and identify the top 5 topics related to {topic_area}. For each topic, provide the following details:
        - Topic Name
        - A brief description of the topic as a sentence
        - Frequency (the number of times the topic appears)
        - Importance (a score indicating the relevance or significance of the topic)
        - Example Mentions (examples of sentences or paragraphs where the topic is mentioned)
        - Related topics within in the content sources
        - Source (the source of the example mentions, including file name or URL)

        Focus your analysis solely on the content embedded within the EmbedChain database, without referring to any external sources. If the data does not exist don't make it up say I that you dont have information.
        """,
        "name": "top_topics"
    }
]

# Process the query and generate the report
report_content = ""
chat_history = []

# Top Topics Identification
query_data = queries[0]
query = query_data["query"]
chat_history.append({"role": "user", "content": query})
app_response = app.query(query, chat_history=chat_history)
chat_history.append({"role": "assistant", "content": app_response})

if num_documents > 0:
    # Generate statistics table for Chroma database in Markdown format
    chroma_statistics_table = f"""
    ## Chroma Database Statistics

    | Metric                 | Value              |
    |------------------------|--------------------|
    | Number of Documents    | {num_documents}    |
    | Average Document Length| {sum(len(data['text']) for data in file_data) / num_documents:.2f} characters |
    | Maximum Document Length| {max(len(data['text']) for data in file_data)} characters |
    | Minimum Document Length| {min(len(data['text']) for data in file_data)} characters |
    """

    # Generate statistics table for EmbedChain database in Markdown format
    statistics_table = f"""
    ## EmbedChain Database Statistics

    | Metric                 | Value              |
    |------------------------|--------------------|
    | Number of Documents    | {num_documents}    |
    """

    # Combine report content with statistics tables
    report_content = app_response + statistics_table + chroma_statistics_table
else:
    print(Fore.RED + "No documents were found or embedded." + Style.RESET_ALL)
    report_content = app_response

# Save the report content along with the statistics table
output_directory = "output"
os.makedirs(output_directory, exist_ok=True)
report_path = os.path.join(output_directory, "topic_analysis_report.md")
try:
    with open(report_path, "w") as report_file:
        report_file.write(report_content)
    print(Fore.CYAN + f"Report with statistics table has been saved to {report_path}" + Style.RESET_ALL)
except Exception as e:
    print(Fore.RED + "Error writing report:" + Style.RESET_ALL, e)