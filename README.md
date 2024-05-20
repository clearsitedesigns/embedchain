# EmbedChain: Service Design Source Analysis

This project demonstrates how to use EmbedChain to embed text data from various file types and directories, capturing source metadata, and analyzing the top topics within the embedded content. The goal is to provide a comprehensive overview of the content landscape, revealing key areas of focus and potential connections for further investigation.

## Installation

```bash
pip install embedchain PyPDF2 markdown tqdm
```
```


### Step-by-Step Explanation

#### Setup and Configuration:

* Imports necessary libraries (like `os`, `json`, `embedchain`, etc.)
* Defines a configuration dictionary (`config`) for the EmbedChain app, specifying the language model (LLM), embedder, vector database, and chunking settings
* Removes any existing database to start fresh
* Initializes the EmbedChain app using the provided configuration

#### Document Reading and Conversion:

* Defines a function (`read_files_from_directory`) to:
    + Traverse a specified directory (`directory_path`)
    + Read the contents of `.txt`, `.md`, and `.pdf` files
    + Convert markdown content to HTML
    + Extract text from PDFs
    + Store the text and source information in a list (`file_data`)

#### Embedding and Adding to Database:

* Iterates through each document in `file_data`
    + Assigns a unique ID (`document_id`)
    + Creates metadata including the source and ID
    + Embeds the document's text using the EmbedChain app and stores it in the vector database, associating the metadata with it

#### Topic Analysis Query:

* Defines a query (`queries`) that instructs the LLM to analyze the embedded content and identify the top topics, providing details like topic name, frequency, importance, example mentions, and source

#### Query Processing and Report Generation:

* Sets a system instruction to guide the LLM's behavior
* Initializes an empty string (`report_content`) to store the report
* Executes the query using the EmbedChain app
* Parses the response from the LLM, extracting the top topics
* Constructs a markdown-formatted report (`report_content`) with the extracted topic details

#### Saving the Report:

* Specifies the report's filename (`topic_analysis.md`)
* Writes the markdown report to the specified file
* Prints a confirmation message
**Libraries Used:**

- `embedchain`: For document embedding, storage, and querying.
- `os`: For file and directory operations.
- `json`: For handling JSON data.
- `shutil`: For directory removal.
- `tqdm`: For progress bar visualization.
- `markdown`: For markdown to HTML conversion.
- `PyPDF2`: For PDF text extraction.

**How to Use:**

1. **Configure:**
   - Set the `directory_path` variable to the directory containing your documents.
   - Customize the `config` dictionary to adjust embedding settings, language model, etc.
2. **Run:**
   - Execute the script.
3. **Output:**
   - A markdown report named `topic_analysis.md` will be generated in the same directory as the script, containing the identified top topics.
