#!/usr/bin/env bash
set -e

PYTHON_VERSION="3.14"
BUILD_DIR="lambda_build"
ZIP_NAME="lambda_bundle.zip"
SRC_DIR="kl_mcp_rag"

echo "Cleaning previous build..."
rm -rf $BUILD_DIR $ZIP_NAME

echo "Creating build directory..."
mkdir -p $BUILD_DIR

echo "Installing dependencies..."
uv pip install \
  --python python$PYTHON_VERSION \
  --target $BUILD_DIR \
  -r pyproject.toml

echo "Copying source code..."
cp -R $SRC_DIR $BUILD_DIR/

echo "Creating deployment zip..."
cd $BUILD_DIR
zip -r ../$ZIP_NAME .
cd ..

echo "Lambda zip created: $ZIP_NAME"