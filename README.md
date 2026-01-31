Set up and install with uv : 

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

b) is slightly faster build. 

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




