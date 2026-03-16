import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv()

S3_BUCKET = os.getenv("S3_BUCKET")

print("Using bucket:", S3_BUCKET)

s3 = boto3.client("s3")

bedrock = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1"
)

MODEL_ID = "amazon.titan-embed-text-v2:0"


def generate_embedding(text):

    body = json.dumps({
        "inputText": text
    })

    response = bedrock.invoke_model(
        body=body,
        modelId=MODEL_ID,
        accept="application/json",
        contentType="application/json"
    )

    result = json.loads(response["body"].read())

    return result["embedding"]


def process_chunks():

    response = s3.list_objects_v2(
        Bucket=S3_BUCKET,
        Prefix="chunks/"
    )

    contents = response.get("Contents", [])

    print("Found chunk files:", len(contents))

    for obj in contents:

        key = obj["Key"]

        if key.endswith(".txt"):

            print("Embedding:", key)

            file_obj = s3.get_object(
                Bucket=S3_BUCKET,
                Key=key
            )

            text = file_obj["Body"].read().decode("utf-8")

            embedding = generate_embedding(text)

            embedding_key = key.replace(
                "chunks/",
                "embeddings/"
            ).replace(".txt", ".json")

            s3.put_object(
                Bucket=S3_BUCKET,
                Key=embedding_key,
                Body=json.dumps({
                    "text": text,
                    "embedding": embedding
                })
            )

            print("Saved:", embedding_key)


if __name__ == "__main__":
    process_chunks()