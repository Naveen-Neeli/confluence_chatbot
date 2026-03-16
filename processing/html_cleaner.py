import boto3
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()

S3_BUCKET = os.getenv("S3_BUCKET")

print("Using bucket:", S3_BUCKET)

s3 = boto3.client("s3")

def html_to_text(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator=" ", strip=True)

def process_documents():

    response = s3.list_objects_v2(
        Bucket=S3_BUCKET,
        Prefix="raw/"
    )

    if "Contents" not in response:
        print("No files found in raw/")
        return

    for obj in response["Contents"]:

        key = obj["Key"]

        # Skip the folder placeholder
        if key.endswith("/"):
            continue

        print("Processing:", key)

        file_obj = s3.get_object(
            Bucket=S3_BUCKET,
            Key=key
        )

        html = file_obj["Body"].read().decode("utf-8")

        text = html_to_text(html)

        new_key = key.replace("raw/", "cleaned/").replace(".html", ".txt")

        s3.put_object(
            Bucket=S3_BUCKET,
            Key=new_key,
            Body=text
        )

        print("Saved:", new_key)


if __name__ == "__main__":
    process_documents()