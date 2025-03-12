# Diploma Thesis: RAG for WIIM

## 📌 Description

This project is a Retrieval-Augmented Generation (RAG) model designed to provide easy access to data from the Chair of Business Information Systems, specifically in Information Management. It includes:

- A pipeline for data preparation (parsing and uploading all documents to an S3 bucket).
- Three versions of the RAG model:
  - **V1.0**: First version after the first iteration of evolutionary prototyping.
  - **V2.0**: Version after the second iteration.
  - **V3.0**: Final version.

## 🚀 Installation

### Prerequisites

Ensure you have the following installed:

- Python (latest stable version recommended)
- Dependencies listed in `requirements.txt`

### Installation Steps

```bash
# Clone the repository
git clone https://github.com/salladora/DiplomaThesisRAG.git

# Navigate into the project folder
cd DiplomaThesisRAG

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt
```

## 🔥 How to Run

### General Setup

1. Set up an `EnvVariables.env` file with AWS access credentials including:
   - `Llama_Cloud_API_Key`
   - `AWS_Access_Key_ID`
   - `AWS_Secret_Access_Key`
   - `AWS_Default_Region`

### Data Preparation

1. **Set up the config file** with the path to the `.env` file and the S3 bucket name.
2. **Upload files to be processed**:
   ```bash
   python uploadUnparsedS3.py
   ```
   - Set variables: local folder path and destination folder in S3.
3. **Parse all documents**:
   ```bash
   python parseDBToDB.py
   ```
   - Set source folder variable to the S3 folder containing unparsed docs.
   - Set destination folder variable to define the output folder name.
4. **Clean parsed metadata**:
   ```bash
   python cleanParsedMetadata.py
   ```
   - Set source folder to the folder containing the parsed documents.

### RAG Model

**Same setup for all versions:**

#### Indexing

1. **Set up the config** with the following values
   ```python
   pc_api = "" # Pinecone API Key
   open_ai_api = "" # OpenAI API Key
   pc_index_name = "" # Name of the destination Pinecone Index
   namespace = "" # Name of the destination Pinecone Namespace
   s3_bucket_name = "" # Name of the source S3 Bucket
   source_folder = r"" # Path to the S3 source folder
   ```
2. **Run the indexing script in the **``** folder**:
   ```bash
   python Indexing_Unit/main.py
   ```
   ⚠ **Important:** Unique vector IDs are generated following a set pattern. Running the program multiple times with the same namespace will override previously stored vectors. To prevent this, modify line 35 in `embedding.py` by replacing `x` with a unique identifier for each run.

#### Querying

1. **Set up the config** with the following values:
   ```python
   OPENAI_API_KEY = ""
   PINECONE_API_KEY = ""
   PINECONE_ENV = "" # Pinecone Environment Region, e.g., "us-east-1"
   PINECONE_INDEX_NAME = ""
   PINECONE_NAMESPACE = ""
   ```
2. **Run the query script in the **``** folder**:
   ```bash
   python Querying_Unit/main.py
   ```
3. **Enter your query** when prompted in the console.

## 🛠 Features

- Operates in the **German language**.
- Displays **generated subqueries**.
- Provides **documents used to generate the response**.

## 📜 License

This project is licensed under the **MIT License**.

## 📞 Author Info

- **GitHub**: [salladora](https://github.com/maya)

