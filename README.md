# EmbedChain: Service Design Source Analysis

This project demonstrates how to use EmbedChain to embed text data from various file types and directories, capturing source metadata, and analyzing the top topics within the embedded content. The goal is to provide a comprehensive overview of the content landscape, revealing key areas of focus and potential connections for further investigation.

## Installation

```bash
pip install embedchain PyPDF2 markdown tqdm
```


# EmbedChain Topic Analysis Script

## Step-by-Step Explanation

### Setup and Configuration
1. **Imports necessary libraries**:
   - `os`, `json`, `shutil`, `sys`
   - `embedchain`, `tqdm`, `markdown`, `PyPDF2`

2. **Defines a configuration dictionary (`config`) for the EmbedChain app**:
   - Specifies the language model (LLM), embedder, vector database, and chunking settings.

3. **Removes any existing database to start fresh**:
   - Deletes the specified vector database directory if it exists.

4. **Initializes the EmbedChain app using the provided configuration**:
   - Uses the `App.from_config(config=config)` method.

### Document Reading and Conversion
1. **Defines a function (`read_files_from_directory`) to**:
   - Traverse a specified directory (`directory_path`).
   - Read the contents of `.txt`, `.md`, and `.pdf` files.
   - Convert markdown content to HTML.
   - Extract text from PDFs.
   - Store the text and source information in a list (`file_data`).

### Embedding and Adding to Database
1. **Iterates through each document in `file_data`**:
   - Assigns a unique ID (`document_id`).
   - Creates metadata including the source and ID.
   - Embeds the document's text using the EmbedChain app and stores it in the vector database, associating the metadata with it.

### Topic Analysis Query
1. **Defines a query (`queries`) that instructs the LLM to**:
   - Analyze the embedded content.
   - Identify the top topics.
   - Provide details like topic name, frequency, importance, example mentions, and source.

### Query Processing and Report Generation
1. **Sets a system instruction to guide the LLM's behavior**.
2. **Initializes an empty string (`report_content`) to store the report**.
3. **Executes the query using the EmbedChain app**.
4. **Parses the response from the LLM**:
   - Extracts the top topics.
5. **Constructs a markdown-formatted report (`report_content`) with the extracted topic details**.

### Saving the Report
1. **Specifies the report's filename (`topic_analysis.md`)**.
2. **Writes the markdown report to the specified file**.
3. **Prints a confirmation message**.

## Libraries Used
- **embedchain**: For document embedding, storage, and querying.
- **os**: For file and directory operations.
- **json**: For handling JSON data.
- **shutil**: For directory removal.
- **tqdm**: For progress bar visualization.
- **markdown**: For markdown to HTML conversion.
- **PyPDF2**: For PDF text extraction.

## How to Use

### Configure:
1. **Set the `directory_path` variable** to the directory containing your documents.
2. **Customize the `config` dictionary** to adjust embedding settings, language model, etc.

### Run:
1. **Execute the script**.

### Output:
1. **A markdown report named `topic_analysis.md`** will be generated in the same directory as the script, containing the identified top topics.
