Set up and install with uv : 
local: 
uv venv
source .venv/bin/activate (macOS)
.venv\Scripts\activate (Windows)
uv pip install -r pyproject.toml

build for lamda: (macOS)
run chmod +x build_lambda_zip.sh in terminal to make shell script executable (once) 

run ./build_lambda_zip.sh in terminal 

upload zip to aws. 



Running the tool: 

lcoally (vs code): 
- launch config set up to run: "Debug Pipeline",

Lamda ... TBC! 



