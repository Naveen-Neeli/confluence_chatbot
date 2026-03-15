import os
import boto3
from atlassian import Confluence
from dotenv import load_dotenv

# load environment variables
load_dotenv()

CONFLUENCE_URL = os.getenv("CONFLUENCE_URL")
CONFLUENCE_EMAIL = os.getenv("CONFLUENCE_EMAIL")
CONFLUENCE_API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")
S3_BUCKET = os.getenv("S3_BUCKET")

# connect to Confluence
confluence = Confluence(
    url=CONFLUENCE_URL,
    username=CONFLUENCE_EMAIL,
    password=CONFLUENCE_API_TOKEN
)

# connect to S3
s3 = boto3.client("s3")


def fetch_pages(space_key):

    pages = confluence.get_all_pages_from_space(
        space_key,
        start=0,
        limit=50
    )

    print(f"Found {len(pages)} pages")

    for page in pages:

        page_id = page["id"]
        title = page["title"]

        page_data = confluence.get_page_by_id(
            page_id,
            expand="body.storage"
        )

        html = page_data["body"]["storage"]["value"]

        s3.put_object(
            Bucket=S3_BUCKET,
            Key=f"raw/{page_id}.html",
            Body=html
        )

        print(f"Uploaded: {title}")


if __name__ == "__main__":

    # your space key from the URL
    fetch_pages("MFS")