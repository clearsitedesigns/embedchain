import os
import json
import shutil
import sys
from embedchain import App
from tqdm import tqdm
import markdown
import PyPDF2

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
            "collection_name": "service-test",
            "dir": "serviceDBTest-2",
            "allow_reset": True
        }
    },
    "chunker": {
        "chunk_size": 350,
        "chunk_overlap": 100,
        "length_function": "len",
        "min_chunk_size": 300
    }
}

# Remove existing database directory if it exists
if os.path.exists(config["vectordb"]["config"]["dir"]):
    shutil.rmtree(config["vectordb"]["config"]["dir"])

# Initialize EmbedChain app
app = App.from_config(config=config)

# Path to your directory containing various file types
directory_path = "/Users/imaginethepoet/Documents/Github/localGPTPrest/GRAPH"

# Variable to check for a particular topic source
topic_area = " Neurophysiology"

# Function to read text from various file types, including subdirectories
def read_files_from_directory(directory):
    file_data = []
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            if filename.endswith(".txt"):
                with open(filepath, 'r') as file:
                    text_content = file.read()
                    file_data.append({"text": text_content, "source": filepath})
            elif filename.endswith(".md"):
                with open(filepath, 'r') as file:
                    md_content = file.read()
                    html_content = markdown.markdown(md_content)
                    file_data.append({"text": html_content, "source": filepath})
            elif filename.endswith(".pdf"):
                with open(filepath, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    pdf_text = ''
                    for page in range(len(reader.pages)):
                        pdf_text += reader.pages[page].extract_text()
                    file_data.append({"text": pdf_text, "source": filepath})
    return file_data

# Read text data from directory
file_data = read_files_from_directory(directory_path)

# Embed the data and add it to the collection
for idx, data in enumerate(file_data):
    document_id = f"doc_{idx}"
    metadata = {"source": data["source"], "document_id": document_id}
    app.add(data["text"], metadata=metadata)
    print(f"Added document {document_id} to collection with source {data['source']}.")
    sys.stdout.flush()

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

system_instruction = f"""
As an expert in content analysis, your task is to examine the entire content embedded in the EmbedChain database and provide the requested information based on the given query, focusing specifically on topics related to {topic_area}.

Focus your analysis solely on the content embedded within the EmbedChain database, without referring to any external sources.
"""

# Process the query and generate the report
report_content = ""
chat_history = []

# Top Topics Identification
query_data = queries[0]
query = query_data["query"]
chat_history.append({"role": "user", "content": query})
app_response = app.query(query, chat_history=chat_history)
chat_history.append({"role": "assistant", "content": app_response})

# Debugging: Print the response from app.query
print("App Response:")
print(app_response)
sys.stdout.flush()

# Save the exact response to the file
report_path = "/Users/imaginethepoet/Documents/Github/localGPTPrest/topic_analysis2.md"

try:
    with open(report_path, "w") as report_file:
        report_file.write(app_response)
    print(f"Report has been saved to {report_path}")
    sys.stdout.flush()
except Exception as e:
    print("Error writing report:", e)
    sys.stdout.flush()
