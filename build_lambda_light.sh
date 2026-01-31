# v2 binary installs (numpy) for AWS Lambda on Linux ARM64 architecture without Docker

#!/usr/bin/env bash
set -e

PYTHON_VERSION="3.14"
BUILD_DIR="lambda_build_v2"
ZIP_NAME="lambda_bundle_v2.zip"
SRC_DIR="kl_mcp_rag"

# Target platform for AWS Lambda on ARM64: OS + CPU
TARGET_PLATFORM="aarch64-unknown-linux-gnu"

echo "Cleaning previous build..."
rm -rf "$BUILD_DIR" "$ZIP_NAME"

echo "Ensuring uv is installed..."

echo "Installing dependencies for AWS Lambda (Linux ARM64)..."
uv pip install \
  --python python$PYTHON_VERSION \
  --python-platform "$TARGET_PLATFORM" \
  --only-binary=:all: \
  --target "$BUILD_DIR" \
  -r pyproject.toml

echo "Copying source code..."
cp -R "$SRC_DIR" "$BUILD_DIR/"

echo "Creating deployment zip..."
python3 - << 'EOF'
import zipfile, os

zip_path = "lambda_bundle_v2.zip"
base_dir = "lambda_build"

with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
    for root, _, files in os.walk(base_dir):
        for f in files:
            full = os.path.join(root, f)
            z.write(full, arcname=os.path.relpath(full, base_dir))
EOF

echo "Lambda zip created: $ZIP_NAME"
