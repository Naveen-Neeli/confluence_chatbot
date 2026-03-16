import streamlit as st
import faiss
import json
import boto3
import numpy as np

bedrock = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1"
)

EMBED_MODEL = "amazon.titan-embed-text-v2:0"
LLM_MODEL = "anthropic.claude-3-haiku-20240307-v1:0"


def generate_embedding(text):

    body = json.dumps({
        "inputText": text
    })

    response = bedrock.invoke_model(
        modelId=EMBED_MODEL,
        body=body,
        accept="application/json",
        contentType="application/json"
    )

    result = json.loads(response["body"].read())

    return np.array(result["embedding"]).astype("float32")


def search_index(question_embedding):

    index = faiss.read_index("vector_store/faiss.index")

    with open("vector_store/chunks.json") as f:
        chunks = json.load(f)

    distances, indices = index.search(
        np.array([question_embedding]),
        k=3
    )

    results = []

    for i in indices[0]:
        results.append(chunks[i])

    return results


def ask_llm(question, context):

    prompt = f"""
You are a helpful assistant answering questions from internal documentation.

Context:
{context}

Question:
{question}

Answer clearly using the context.
"""

    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 300,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    })

    response = bedrock.invoke_model(
        modelId=LLM_MODEL,
        body=body,
        accept="application/json",
        contentType="application/json"
    )

    result = json.loads(response["body"].read())

    return result["content"][0]["text"]


# STREAMLIT UI

st.title("Confluence AI Assistant")

st.write("Ask questions about your Confluence documentation")

question = st.text_input("Ask a question")

if st.button("Ask"):

    if question:

        with st.spinner("Thinking..."):

            q_embedding = generate_embedding(question)

            chunks = search_index(q_embedding)

            context = "\n\n".join(chunks)

            answer = ask_llm(question, context)

        st.subheader("Answer")

        st.write(answer)