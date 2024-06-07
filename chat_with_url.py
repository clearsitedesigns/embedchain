import os
import json
import sys
from embedchain import App
from colorama import init
from loguru import logger
from tqdm import tqdm
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# Initialize colorama
init(autoreset=True)

# Configure loguru
logger.add("debug.log", format="{time} {level} {message}", level="DEBUG", rotation="10 MB", retention="10 days")

# Initialize Rich console
console = Console()

# Function to prompt user for input with a default value
def prompt_with_default(prompt, default):
    user_input = input(f"{prompt} (default: {default}): ")
    return user_input.strip() or default

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
            "collection_name": "chattyweb16",
            "dir": "chattynew16",
            "allow_reset": True
        }
    }
}

# Initialize EmbedChain app with the configuration
logger.info("Initializing EmbedChain app with the configuration.")
app = App.from_config(config=config)

# Add data source (URL) to the app
url = prompt_with_default("Enter the URL to chat with", "https://www.forbes.com/profile/elon-musk")
logger.info(f"Adding URL to app: {url}")
app.add(url)

# Define system instructions
system_instructions = """
You are an AI assistant grounded in the data source provided.
When answering user queries, provide information only from the given data source.
If the data source does not contain enough information to answer a query, respond with:
"The data source doesn't have enough information to answer this."
"""

# Define chat history with system instructions
chat_history = [{"role": "system", "content": system_instructions}]

# Function to query the app and handle potential errors
def query_app(query, history=None):
    try:
        response = app.query(query, chat_history=history)
        logger.debug(f"App response: {response}")
        return response
    except Exception as e:
        logger.error(f"Error querying app: {e}")
        return None

# Function to calculate context relevance
def calculate_context_relevance(topic):
    # Implement your logic to calculate context relevance score
    # You can use techniques like semantic similarity or keyword matching
    # between the question and the retrieved context
    return 0.8

# Function to calculate semantic similarity
def calculate_semantic_similarity(answer, context):
    # Implement your logic to calculate semantic similarity between answer and context
    # You can use libraries like spaCy, NLTK, or sentence transformers
    return 0.75

# Function to check if a source is relevant
def is_relevant(source):
    # Implement your logic to determine if a source is relevant
    # You can use criteria like the presence of keywords or the source's reliability
    return True

# Function to calculate confidence score
def calculate_confidence_score(topic):
    context_relevance = calculate_context_relevance(topic)
    model_confidence = topic.get("model_confidence", 0.0)
    confidence_score = (context_relevance + model_confidence) / 2 * 100
    return confidence_score

# Function to calculate grounding score
def calculate_grounding_score(topic):
    answer = topic.get("answer", "")
    context = topic.get("context", "")
    similarity_score = calculate_semantic_similarity(answer, context)
    grounding_score = similarity_score * 100
    return grounding_score

# Function to calculate K Sym (Knowledge Symmetry)
def calculate_k_sym(topic):
    context_sources = topic.get("context_sources", [])
    total_sources = len(context_sources)
    relevant_sources = sum(1 for source in context_sources if is_relevant(source))
    if total_sources == 0:
        return 0
    k_sym = relevant_sources / total_sources * 100
    return k_sym

# Query the data source for top 5 topics with cited examples and grounding scores
top_topics_query = """
Analyze the data source and identify the top 5 topics based on frequency and relevance.
For each topic, provide a brief description, grounding score, and cited examples from the data source, if available.
Include metadata such as source URLs and timestamps for each example.
If no examples are found, mention that no specific examples were found for that topic.
"""

top_topics_response = query_app(top_topics_query)

# Check if the response is empty
if not top_topics_response:
    logger.error("Received an empty response from the query.")
    console.print("[bold red]Received an empty response from the query.[/bold red]")
    sys.exit(1)

# Check if the response is a valid JSON string
try:
    top_topics_response = json.loads(top_topics_response)
    logger.debug("Successfully parsed JSON response.")
except json.JSONDecodeError as e:
    logger.debug(f"Response is not a valid JSON string: {e}")
    top_topics_response = {"response": top_topics_response}

def format_topics_response(response):
    formatted_response = ""
    if isinstance(response, dict) and 'topics' in response:
        topics = response.get("topics", [])
        for i, topic in enumerate(topics, start=1):
            title = topic.get("title", f"Topic {i}")
            description = topic.get("description", "No description available.")
            grounding_score = calculate_grounding_score(topic)
            confidence_score = calculate_confidence_score(topic)
            k_sym = calculate_k_sym(topic)
            examples = topic.get("examples", [])

            formatted_response += f"[bold cyan]{'━'*100}[/bold cyan]\n"
            formatted_response += f"[bold yellow]Topic {i}: {title}[/bold yellow]\n"
            formatted_response += f"[green]{description}[/green]\n\n"
            formatted_response += f"[bold]Confidence Score:[/bold] {confidence_score:.1f}% | [bold]Grounding Score:[/bold] {grounding_score:.1f}% | [bold]K Sym:[/bold] {k_sym:.1f}%\n\n"
            formatted_response += f"[bold]Sources:[/bold]\n"
            if examples:
                for idx, example in enumerate(examples, 1):
                    example_text = example.get("text", "No example text available.")
                    source_url = example.get("source_url", "No source URL available.")
                    formatted_response += f"    {idx}. [italic]{example_text}[/italic] ([blue][link={source_url}]{source_url}[/link][/blue])\n"
            else:
                formatted_response += "    - No specific examples were found for this topic.\n"
            formatted_response += f"[bold cyan]{'━'*100}[/bold cyan]\n\n"
    else:
        formatted_response += response.get("response", "No response available.")
    
    return formatted_response

# Print the initial message with top 5 topics and examples
try:
    formatted_response = format_topics_response(top_topics_response)
    logger.debug("Formatted response generated successfully.")
    console.print(Panel(
        Text("Initial Message", style="bold yellow"),
        expand=False,
        border_style="bold"
    ))
    console.print(formatted_response)
    print()
except Exception as e:
    logger.error(f"Error formatting response: {e}")
    console.print("Error formatting response.", style="bold red")
    sys.exit(1)

# Start chat loop
console.print("[bold green]You can start chatting. Type 'exit' to end the conversation.[/bold green]")
while True:
    user_input = input("[blue]You:[/blue] ")
    if user_input.lower() == "exit":
        console.print("[bold green]Goodbye![/bold green]")
        break
    else:
        chat_history.append({"role": "user", "content": user_input})
        app_response = query_app(user_input, history=chat_history)
        
        if not app_response:
            console.print("[bold red]Error querying app.[/bold red]")
            continue
        
        if "The data source doesn't have enough information to answer this." in app_response:
            chat_history.append({"role": "assistant", "content": app_response})
            console.print(f"[bold red]Assistant:[/bold red] {app_response}")
        else:
            chat_history.append({"role": "assistant", "content": app_response})
            console.print(f"[bold magenta]Assistant:[/bold magenta] {app_response}")

# Use tqdm to monitor the embedding process
for i in tqdm(range(100), desc="Embedding progress"):
    import time
    time.sleep(0.1)

logger.info("Embedding process completed.")
