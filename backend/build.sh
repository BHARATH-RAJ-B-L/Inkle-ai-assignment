#!/bin/bash
# Render build script - installs dependencies with specific flags to avoid Rust compilation

# Upgrade pip
pip install --upgrade pip

# Install dependencies one by one to avoid Rust compilation issues
pip install fastapi==0.109.0
pip install "uvicorn[standard]==0.27.0"
pip install httpx==0.26.0
pip install pydantic==2.6.0
pip install pydantic-settings==2.1.0
pip install python-dotenv==1.0.0

# Install LangChain packages with --only-binary flag to avoid building from source
pip install --only-binary=:all: langchain-core==0.1.52 || pip install langchain-core==0.1.52 --no-build-isolation
pip install --only-binary=:all: langchain==0.1.20 || pip install langchain==0.1.20 --no-build-isolation
pip install --only-binary=:all: langchain-openai==0.1.7 || pip install langchain-openai==0.1.7 --no-build-isolation
pip install --only-binary=:all: langgraph==0.0.62 || pip install langgraph==0.0.62 --no-build-isolation

echo "✅ All dependencies installed successfully!"
