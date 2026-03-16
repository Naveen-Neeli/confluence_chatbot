Here is the **complete documentation in one continuous block** so you can copy it directly into a README or documentation file.

---

# Confluence RAG Chatbot using AWS Bedrock

## Overview

This project implements a **Retrieval-Augmented Generation (RAG) chatbot** that answers questions based on documentation stored in Confluence.

The system extracts Confluence documentation pages, processes them, converts them into vector embeddings, and retrieves relevant information to generate accurate answers using a large language model.

Users can ask natural language questions, and the chatbot retrieves relevant document chunks before generating responses grounded in internal documentation.

The system uses **Amazon Bedrock** for embeddings and LLM inference.

---

# Architecture

The system follows a standard **RAG architecture**.

```
User Question
      ↓
Generate Embedding
      ↓
Vector Search (FAISS)
      ↓
Retrieve Relevant Document Chunks
      ↓
Send Context + Question to LLM
      ↓
Generate Answer
```

Full pipeline architecture:

```
Confluence
   ↓
Ingestion Script
   ↓
S3 Raw HTML Storage
   ↓
HTML Cleaning
   ↓
Text Chunking
   ↓
Embedding Generation
   ↓
Vector Index
   ↓
Retriever
   ↓
LLM
   ↓
Chatbot
```

---

# Technology Stack

Cloud Platform: AWS
LLM Platform: Amazon Bedrock
Embedding Model: Amazon Titan Embeddings
LLM Model: Claude 3 Haiku
Vector Search: FAISS
Storage: Amazon S3
Language: Python
Parsing Library: BeautifulSoup
Environment Management: Conda / Virtual Environment

---

# Project Structure

```
confluence_chatbot/
│
├── ingestion/
│   └── confluence_loader.py
│
├── processing/
│   ├── html_cleaner.py
│   └── chunker.py
│
├── embeddings/
│   └── generate_embeddings.py
│
├── vector_store/
│   └── build_index.py
│
├── chat.py
├── .env
└── README.md
```

---

# System Workflow

## 1. Confluence Data Ingestion

The ingestion script connects to the Confluence API and downloads documentation pages.

Each page's HTML content is stored in Amazon S3.

Example output:

```
S3/raw/
   page1.html
   page2.html
   page3.html
```

---

## 2. HTML Cleaning

Confluence pages contain HTML markup and metadata that are not useful for AI processing.

The system uses BeautifulSoup to parse the HTML and extract clean readable text.

Example transformation:

```
HTML Document
      ↓
Clean Text Content
```

Example output:

```
S3/cleaned/
   page1.txt
   page2.txt
```

---

## 3. Document Chunking

Large documents are split into smaller text chunks.

Chunking improves retrieval quality because LLMs perform better when provided with smaller, focused context.

Example:

```
Document
   ↓
Chunk 1
Chunk 2
Chunk 3
```

Chunks are stored in S3.

```
S3/chunks/
   page1_chunk_1.txt
   page1_chunk_2.txt
   page2_chunk_1.txt
```

---

## 4. Embedding Generation

Each chunk is converted into a vector embedding using Amazon Titan Embeddings through Amazon Bedrock.

Embeddings represent the semantic meaning of the text.

Example vector representation:

```
[0.23, -0.12, 0.91, ...]
```

Stored as:

```
S3/embeddings/
   chunk_1.json
   chunk_2.json
```

Each embedding file contains:

```
{
  "text": "chunk content",
  "embedding": [vector values]
}
```

---

## 5. Vector Index Creation

All embeddings are loaded and stored in a FAISS vector index.

FAISS enables efficient similarity search across thousands of embeddings.

Output files:

```
vector_store/
   faiss.index
   chunks.json
```

These files serve as the local vector database used during retrieval.

---

## 6. Question Answering

When a user asks a question, the system performs the following steps:

1. Convert the question into an embedding vector.
2. Search the FAISS index for similar vectors.
3. Retrieve the most relevant document chunks.
4. Combine the chunks with the user question.
5. Send the combined context to the LLM.
6. Generate a final answer.

Example user query:

```
User: What is the first application requirement?
```

The system retrieves the relevant section from documentation and generates a contextual answer.

---

# Example Interaction

```
Ask a question: What is the first application?

Answer:

The first application requirement is enabling real-time order processing.
The system must support high transaction volumes while maintaining reliable order tracking and monitoring.
```

---

# Key Features

Automated ingestion of Confluence documentation
Semantic search using vector embeddings
Retrieval-Augmented Generation architecture
Context-aware question answering
Cloud-based scalable architecture
Integration with AWS Bedrock foundation models

---

# Setup Instructions

## 1. Clone Repository

```
git clone <repository-url>
cd confluence_chatbot
```

---

## 2. Create Environment

```
conda create -n rag-chatbot python=3.10
conda activate rag-chatbot
```

---

## 3. Install Dependencies

```
pip install boto3 numpy faiss-cpu python-dotenv beautifulsoup4
```

---

## 4. Configure Environment Variables

Create a `.env` file:

```
AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY
AWS_SECRET_ACCESS_KEY=YOUR_SECRET_KEY
S3_BUCKET=my-workspace-nn
```

---

## 5. Run the Pipeline

### Ingest Confluence pages

```
python ingestion/confluence_loader.py
```

### Clean HTML

```
python processing/html_cleaner.py
```

### Chunk documents

```
python processing/chunker.py
```

### Generate embeddings

```
python embeddings/generate_embeddings.py
```

### Build vector index

```
python vector_store/build_index.py
```

### Run chatbot

```
python chat.py
```

---

# Limitations

FAISS vector index is stored locally rather than in a distributed vector database
Ingestion process is manual and not automatically triggered by document updates
The chatbot currently runs only in a terminal interface

---

# Future Improvements

## Web Interface

Build a web UI using Streamlit to allow interactive chat with the documentation.

---

## Automatic Document Sync

Use AWS EventBridge and Lambda to automatically update embeddings whenever Confluence pages change.

---

## Production Vector Database

Replace FAISS with scalable vector storage such as:

OpenSearch
Pinecone
pgvector

---

## Source Citations

Enhance the chatbot to return the original Confluence page link with each answer.

Example output:

```
Answer:
...

Source:
Confluence → Architecture Overview
```

---

# Key Learnings

This project demonstrates:

Retrieval-Augmented Generation architecture
Document preprocessing pipelines
Embedding-based semantic search
Integration with AWS Bedrock foundation models
Vector indexing and similarity search
Building AI-powered knowledge assistants

---

# Conclusion

This project demonstrates how to build an AI-powered knowledge assistant that combines document retrieval with generative AI.

By integrating Confluence documentation, vector embeddings, and large language models, the system can generate accurate and context-aware answers grounded in internal knowledge.

---

If you want, I can also help you create a **much more impressive GitHub README with architecture diagrams and visuals**, which will make the project stand out significantly when recruiters view it.
