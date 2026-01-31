#!/usr/bin/env bash
set -e

PYTHON_VERSION="3.14"
BUILD_DIR="lambda_build"
ZIP_NAME="lambda_bundle.zip"
SRC_DIR="kl_mcp_rag"
LAMBDA_IMAGE="public.ecr.aws/lambda/python:3.14"

echo "Cleaning previous build..."
rm -rf "$BUILD_DIR" "$ZIP_NAME"

echo "Running build inside Lambda Docker image..."

docker run --rm \
  --entrypoint "" \
  -v "$PWD":/work \
  -w /work \
  "$LAMBDA_IMAGE" \
  bash -c "
    set -e

    echo 'Installing uv...'
    pip install -q uv

    echo 'Installing dependencies (Linux-compatible)...'
    uv pip install \
      --python python$PYTHON_VERSION \
      --target $BUILD_DIR \
      -r pyproject.toml

    echo 'Copying source code...'
    cp -R $SRC_DIR $BUILD_DIR/

    echo 'Creating deployment zip (via Python)...'
    python - << 'EOF'
import zipfile, os

zip_path = '$ZIP_NAME'
base_dir = '$BUILD_DIR'

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    for root, _, files in os.walk(base_dir):
        for f in files:
            full = os.path.join(root, f)
            z.write(full, arcname=os.path.relpath(full, base_dir))
EOF
  "

echo "Lambda zip created: $ZIP_NAME"