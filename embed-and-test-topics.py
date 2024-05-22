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

# Define queries for analyzing the top topics
queries = [
    {
        "query": f"""
        Analyze the embedded content and identify the top topics related to {topic_area}. For each topic, provide the following details:
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

def extract_topics_from_response(response):
    topics = []
    lines = response.split("\n")
    current_topic = None
    
    for line in lines:
        if line.startswith("**Topic"):
            if current_topic:
                topics.append(current_topic)
            current_topic = {"topic_name": "", "description": "", "related_topics": "", "frequency": 0, "importance": 0, "example_mentions": [], "source": ""}
            current_topic["topic_name"] = line.split(":")[1].strip()
        elif line.startswith("* Description:"):
            current_topic["description"] = line.split(":")[1].strip()
        elif line.startswith("* Related Topics:"):
            current_topic["related_topics"] = line.split(":")[1].strip()
        elif line.startswith("* Frequency:"):
            current_topic["frequency"] = int(line.split(":")[1].strip())
        elif line.startswith("* Importance:"):
            current_topic["importance"] = float(line.split(":")[1].strip())
        elif line.startswith("\t+"):
            current_topic["example_mentions"].append(line.strip())
        elif line.startswith("* Source:"):
            current_topic["source"] = line.split(":")[1].strip()
    
    if current_topic:
        topics.append(current_topic)
    
    return topics

top_topics = extract_topics_from_response(app_response)
print("Top Topics:")
print(top_topics)

report_content += "## Top Topics\n\n"
for topic in top_topics:
    report_content += f"Topic Name: {topic['topic_name']}\n"
    report_content += f"Description: {topic['description']}\n"
    report_content += f"Related Topics: {topic['related_topics']}\n"
    report_content += f"Frequency: {topic['frequency']}\n"
    report_content += f"Importance: {topic['importance']}\n"
    report_content += "Example Mentions:\n"
    for mention in topic['example_mentions']:
        report_content += f"- {mention}\n"
    report_content += f"Source: {topic['source']}\n"
    report_content += "\n"

print("Report Content:")
print(report_content)

# Specify the path to save your markdown report
report_path = "topic_analysis2.md"

# Write the markdown content to a file
try:
    with open(report_path, "w") as report_file:
        report_file.write(report_content)
    print(f"Report has been saved to {report_path}")
except Exception as e:
    print("Error writing report:", e)
