Created by Preston McCauley - 2024


# EmbedChain: Starter Analysis

This project demonstrates how to use EmbedChain to embed text data from various file types and directories, capturing source metadata, and analyzing the top topics within the embedded content. The goal is to provide a comprehensive overview of the content landscape, revealing key areas of focus and potential connections for further investigation. This needs a local LLM and is setup to use the OLLAMA system 

## Features

- Supports various file types: `.txt`, `.md`, and `.pdf`
- Recursively reads files from subdirectories
- Prompts the user for database name, collection name, and chunking strategy
- Provides a default embedding method for text data
- Allows customization of chunking parameters based on analysis objectives and computational resources
- Appends "_DB" to the database name for clarity
- Generates a report with the top 5 topics related to the specified topic area
- Includes statistics tables for the Chroma and EmbedChain databases in the report
- Saves the report as a Markdown file in the "output" directory
- Utilizes colorama for enhanced terminal output

## Installation

```bash
pip install embedchain PyPDF2 markdown tqdm colorama

Or run requirements.txt



### Step-by-Step Explanation

#### Setup and Configuration

You need to make sure Ollama service is running locally!


1.  **Imports necessary libraries:**
    -   `os`, `json`, `shutil`, `sys`
    -   `embedchain`, `tqdm`, `markdown`, `PyPDF2`, `colorama`
2.  **Defines a configuration dictionary (`config`) for the EmbedChain app:**
    -   Specifies the language model (LLM), embedder, vector database, and chunking settings.
3.  **Initializes the EmbedChain app using the provided configuration:**
    -   Uses the `App.from_config(config=config)` method.
4.  **Prompts the user for database name, collection name, and chunking strategy:**
    -   Appends "_DB" to the user-provided database name.
5.  **Provides a default embedding method for text data.**
6.  **Allows customization of chunking parameters based on analysis objectives and computational resources.**

#### Document Reading and Conversion

1.  **Defines a function (`read_files_from_directory`) to:**
    -   Traverse a specified directory (`directory_path`).
    -   Read the contents of `.txt`, `.md`, and `.pdf` files.
    -   Convert markdown content to HTML.
    -   Extract text from PDFs.
    -   Store the text, source information, and file name in a list (`file_data`).

#### Embedding and Adding to Database

1.  **Iterates through each document in `file_data`:**
    -   Assigns a unique ID (`document_id`).
    -   Creates metadata including the source, ID, and file name.
    -   Embeds the document's text using the EmbedChain app and stores it in the vector database, associating the metadata with it.

#### Topic Analysis Query

1.  **Defines a query (`queries`) that instructs the LLM to:**
    -   Analyze the embedded content.
    -   Identify the top topics.
    -   Provide details like topic name, frequency, importance, example mentions, and source.

#### Query Processing and Report Generation

1.  **Initializes an empty string (`report_content`) to store the report.**
2.  **Executes the query using the EmbedChain app.**
3.  **Parses the response from the LLM:**
    -   Extracts the top topics.
    -   Constructs a markdown-formatted report (`report_content`) with the extracted topic details.
4.  **Generates statistics tables for the Chroma and EmbedChain databases.**

#### Saving the Report

1.  **Specifies the report's filename (`topic_analysis_report.md`).**
2.  **Writes the markdown report to the specified file in the "output" directory.**
3.  **Prints a confirmation message with the report path.**

### Libraries Used

-   `embedchain`: For document embedding, storage, and querying.
-   `os`: For file and directory operations.
-   `json`: For handling JSON data.
-   `shutil`: For directory removal.
-   `tqdm`: For progress bar visualization.
-   `markdown`: For markdown to HTML conversion.
-   `PyPDF2`: For PDF text extraction.
-   `colorama`: For colored terminal output.

### How to Use


1.  python embed-and-test-topics.py
2.  **Configure In Command Window You will be asked** 
    -   Set the `directory_path` variable to the directory containing your documents.
    -   Customize the `config` dictionary to adjust embedding settings, language model, etc.
3.  **Run:**
    -   Execute the script.

### Output:

A markdown report named `topic_analysis_report.md` will be generated in the "output" directory, containing the identified top topics along with statistics tables.

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