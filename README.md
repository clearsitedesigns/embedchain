# EmbedChain: Service Design Source Analysis

This project demonstrates how to use EmbedChain to embed text data from various file types and directories, capturing source metadata, and analyzing the top topics within the embedded content. The goal is to provide a comprehensive overview of the content landscape, revealing key areas of focus and potential connections for further investigation.

## Installation

First, install the necessary Python packages:

```bash
pip install embedchain PyPDF2 markdown tqdm


### Document Topic Analysis Script

This Python script is designed to analyze a collection of documents and extract the top topics. It leverages the `EmbedChain` library for document embedding, storage, and querying.

**Key Functionality:**

1. **Document Ingestion:**
   - Reads text, markdown, and PDF files from a specified directory.
   - Converts markdown to HTML and extracts text from PDFs.

2. **Embedding and Storage:**
   - Embeds the text content of each document using a language model and vector database.
   - Stores the embeddings along with metadata (source, document ID) in a vector database.

3. **Topic Querying:**
   - Defines a query to instruct the language model to identify and analyze the top topics within the embedded documents.

4. **Report Generation:**
   - Executes the query and retrieves the results from the language model.
   - Parses the results and extracts the top topics, their frequency, importance, and example mentions.
   - Generates a markdown report summarizing the extracted topics.

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
