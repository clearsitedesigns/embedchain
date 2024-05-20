import os
import json
import shutil
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
        "chunk_overlap": 100,  # Adjusted to be less than min_chunk_size
        "length_function": "len",
        "min_chunk_size": 300  # Adjusted to be greater than chunk_overlap
    }
}

# Remove existing database directory if it exists
if os.path.exists(config["vectordb"]["config"]["dir"]):
    shutil.rmtree(config["vectordb"]["config"]["dir"])

# Initialize EmbedChain app
app = App.from_config(config=config)

# Path to your directory containing various file types
directory_path = "ServiceDesignSource"

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
    document_id = f"doc_{idx}"  # Unique identifier for each document
    metadata = {"source": data["source"], "document_id": document_id}
    app.add(data["text"], metadata=metadata)  # Adding text content with metadata
    print(f"Added document {document_id} to collection with source {data['source']}.")

# Define queries for analyzing the top topics
queries = [
    {
        "query": """
        Analyze the embedded content and identify the top topics. For each topic, provide the following details:
        - Topic Name
        - Frequency (the number of times the topic appears)
        - Importance (a score indicating the relevance or significance of the topic)
        - Example Mentions (examples of sentences or paragraphs where the topic is mentioned)
        - Source (the source of the example mentions, including file name or URL)

        Focus your analysis solely on the content embedded within the EmbedChain database, without referring to any external sources.
        """,
        "name": "top_topics"
    }
]

system_instruction = """
As an expert in content analysis, your task is to examine the entire content embedded in the EmbedChain database and provide the requested information based on the given query.

Focus your analysis solely on the content embedded within the EmbedChain database, without referring to any external sources.
"""

# Process the query and generate the report
report_content = ""
chat_history = []

# Top Topics Identification
query_data = queries[0]
query = query_data["query"]
chat_history.append({"role": "user", "content": query})
app_response = app.query(query, chat_history=chat_history)  # Assuming this is a correct query
chat_history.append({"role": "assistant", "content": app_response})

# Parse the string response as JSON
try:
    parsed_response = json.loads(app_response)
except json.JSONDecodeError:
    parsed_response = {"response": app_response}

top_topics = parsed_response.get("top_topics", [])
report_content += "## Top Topics\n\n"
for topic in top_topics:
    report_content += f"Topic Name: {topic['topic_name']}\n"
    report_content += f"Frequency: {topic['frequency']}\n"
    report_content += f"Importance: {topic['importance']}\n"
    report_content += "Example Mentions:\n"
    for mention in topic['example_mentions']:
        report_content += f"- {mention}\n"
    report_content += f"Source: {topic['source']}\n"  # Include the source information
    report_content += "\n"

# Specify the path to save your markdown report
report_path = "topic_analysis.md"

# Write the markdown content to a file
with open(report_path, "w") as report_file:
    report_file.write(report_content)

print(f"Report has been saved to {report_path}")
