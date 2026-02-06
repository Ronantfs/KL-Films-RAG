# Note on the project. 

This repo is the code for the backend of https://kl-ai-ui.netlify.app/: 

It is a tool that takes natural language user queries, say from the UI client, and checks against https://kinologue.co.uk 's listings to see what is on. 

The idea here is to provide a more human native interface for seeing what's on. 

In essence, the backend in a pipeline that extracts query params from the users query (film name, cinemas and natural language date expression). 

The film names are matched using RAG against a vector database of the embbeded listing titles from kinologue -- RAG makes sense here are film titles a new and domain specific, so we don;t expect a pre trained LLM to relaibly identify film names. 

Depending on which query params we extract from the users query, we call a suitable determinstic look up function, and formatted string is retunred to the UI client. 

## Codebase: 
The handler can be found at kl_mcp_rag/pipeline_handler.py
See the contents of kl_mcp_rag/rag for the code related to the RAG part of the syste, particualrly the FilmIndex class in kl_mcp_rag/rag/index.py

----

# Set up and install with uv : 

### local: 
uv venv
source .venv/bin/activate (macOS)
.venv\Scripts\activate (Windows)
uv pip install -r pyproject.toml

---

### build for lamda: (macOS)

2) altertive solutions to linux runtime comaptible builds (for lambda)
a) build in linux docker env to select linux wheels (numpy)
b) uv command to select for these wheels 

NOTE b) is faster build. 

#### a) build in linux docker: build_lambda_zip.sh
make executable (once)
- chmod +x build_lambda_zip.sh

run in terminal:
- ./build_lambda_zip.sh 

upload zip to aws. 

#### b) 
see desgin_decision_logs/v4.1_no_docker_run_on_linux.md for detailed notes  

Make executable(run once):
```sh
 chmod +x build_lambda_light.sh
```
execute: 
```sh
./build_lambda_light.sh
```

--> lambda_bundle_v2.zip
-------

# ▶️Running the tool: 

locally (vs code): 
- ensure local build (see top)
- launch config set up to run: "Debug Pipeline",




