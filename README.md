Created by Preston McCauley - 2024


# EmbedChain: Starter Analysis

This project demonstrates how to use EmbedChain to embed text data from various file types and directories, capturing source metadata, and analyzing the top topics within the embedded content. The goal is to provide a comprehensive overview of the content landscape, revealing key areas of focus and potential connections for further investigation. This needs a local LLM and is setup to use the OLLAMA system. 

# EmbedChain Topic Analysis Scripts
 - Added a script example to chat with a website URL.

## Overview

This script allows users to create and manage document databases using EmbedChain, embed text data from various file types, and analyze the embedded content to identify top topics. It also provides a continual chat interface for querying the embedded data.

## Features

- **Database Management**: Create and manage databases for storing embedded documents.
- **Document Embedding**: Embed text data from `.txt`, `.md`, and `.pdf` files.
- **Topic Analysis**: Analyze embedded content to identify top topics related to a user-defined area.
- **Continual Chat Interface**: Interact with the embedded data through a continual chat interface.

## Installation

pip install -r requirements.txt

### Prerequisites

Ensure you have the following installed:

- Conda package manager (Anaconda or Miniconda)

### Install Required Packages

Create a conda environment and activate it:

```sh
conda create --name embedchain_env python=3.10
conda activate embedchain_env

python embed-and-test-topics.py #or the other script specifically for chatting with a web site url, 


A markdown report named `topic_analysis_report.md` will be generated in the "output" directory, containing the identified top topics along with statistics tables.


### Example Output
Enter database name (default: default_database): my_database
Enter collection name (default: default_collection): my_collection
Determine chunking strategy:
Is the data type text? [yes/no] (default: yes): yes
Using default embedding method for text data.
Please enter the full path to the directory containing files to embed: /path/to/your/documents
Please enter the topic area for analysis: AI advancements


### License

This script is open-source and available under the MIT License.

### Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.


### Acknowledgements

-  Ollama used for LLM (any model will do)
-  Huggingface Downlodas the embedding model (using a large model) 
-  EmbedChain - EmbedChain library for embedding and analysis
-   Chroma - Chroma library for vector database management
-   tqdm - Progress bar library
-   colorama - Library for colored terminal output
-   markdown - Markdown processing library
-   PyPDF2 - PDF processing library