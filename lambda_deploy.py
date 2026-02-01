import boto3
from pathlib import Path

LAMBDA_NAME = "kl_ai_v0"
ZIP_PATH = Path("lambda_bundle_v2.zip")
AWS_REGION = "eu-north-1"
AWS_PROFILE = "ronantfs"


def main():
    if not ZIP_PATH.exists():
        raise FileNotFoundError(f"{ZIP_PATH} not found")

    session = boto3.Session(
        profile_name=AWS_PROFILE,
        region_name=AWS_REGION,
    )

    client = session.client("lambda")

    # rb: read binary
    with ZIP_PATH.open("rb") as f:
        response = client.update_function_code(
            FunctionName=LAMBDA_NAME,
            ZipFile=f.read(),
            Publish=True,
        )

    print("Lambda updated")
    print("Version:", response["Version"])


if __name__ == "__main__":
    main()
