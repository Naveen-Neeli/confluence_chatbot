import boto3
import json
import os
import faiss
import numpy as np
from dotenv import load_dotenv

load_dotenv()

S3_BUCKET = os.getenv("S3_BUCKET")

s3 = boto3.client("s3")


def load_embeddings():

    response = s3.list_objects_v2(
        Bucket=S3_BUCKET,
        Prefix="embeddings/"
    )

    vectors = []
    texts = []

    for obj in response.get("Contents", []):

        key = obj["Key"]

        if key.endswith(".json"):

            file_obj = s3.get_object(
                Bucket=S3_BUCKET,
                Key=key
            )

            data = json.loads(file_obj["Body"].read())

            vectors.append(data["embedding"])
            texts.append(data["text"])

    return vectors, texts


def build_index():

    vectors, texts = load_embeddings()

    dimension = len(vectors[0])

    index = faiss.IndexFlatL2(dimension)

    vector_array = np.array(vectors).astype("float32")

    index.add(vector_array)

    faiss.write_index(index, "vector_store/faiss.index")

    with open("vector_store/chunks.json", "w") as f:
        json.dump(texts, f)

    print("Vector index built successfully")


if __name__ == "__main__":
    build_index()