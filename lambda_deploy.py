import boto3
from pathlib import Path

LAMBDA_NAME = "kl_ai_v0"
ZIP_PATH = Path("lambda_bundle_v2.zip")

# build artefact
S3_BUCKET = "kl-ai"
S3_KEY = "lambda_bundle_v2.zip"

AWS_REGION = "eu-north-1"
AWS_PROFILE = "ronantfs"


def main():
    if not ZIP_PATH.exists():
        raise FileNotFoundError(f"{ZIP_PATH} not found")

    session = boto3.Session(
        profile_name=AWS_PROFILE,
        region_name=AWS_REGION,
    )

    s3 = session.client("s3")
    lambda_client = session.client("lambda")

    # 1) Upload zip from disk to S3
    s3.upload_file(
        Filename=str(ZIP_PATH),
        Bucket=S3_BUCKET,
        Key=S3_KEY,
    )

    print(f"Uploaded {ZIP_PATH} to s3://{S3_BUCKET}/{S3_KEY}")

    # 2) Trigger Lambda rebuild from S3 artifact
    response = lambda_client.update_function_code(
        FunctionName=LAMBDA_NAME,
        S3Bucket=S3_BUCKET,
        S3Key=S3_KEY,
        Publish=True,  # create a new immutable version
    )

    print("Lambda updated")
    print("Version:", response["Version"])


if __name__ == "__main__":
    main()
