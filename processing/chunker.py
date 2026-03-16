import boto3
import os
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

S3_BUCKET = os.getenv("S3_BUCKET")

s3 = boto3.client("s3")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

def chunk_documents():

    response = s3.list_objects_v2(
        Bucket=S3_BUCKET,
        Prefix="cleaned/"
    )

    for obj in response.get("Contents", []):

        key = obj["Key"]

        if key.endswith(".txt"):

            print("Reading:", key)

            file_obj = s3.get_object(
                Bucket=S3_BUCKET,
                Key=key
            )

            text = file_obj["Body"].read().decode("utf-8")

            chunks = splitter.split_text(text)

            for i, chunk in enumerate(chunks):

                chunk_key = key.replace(
                    "cleaned/",
                    "chunks/"
                ).replace(".txt", f"_chunk_{i}.txt")

                s3.put_object(
                    Bucket=S3_BUCKET,
                    Key=chunk_key,
                    Body=chunk
                )

                print("Saved:", chunk_key)

if __name__ == "__main__":
    chunk_documents()