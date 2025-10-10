## How to Run `run.sh`

This script sets up and launches the CodebaseAI Docker environment for analysis and experimentation.

### Prerequisites

- Docker and Docker Compose must be installed on your system.
- Clone this repository and ensure you are in the `codebaseai-runner` directory.

### Usage

1. **Make sure `run.sh` is executable:**
	```bash
	chmod +x run.sh
	```

2. **Run the script:**
	```bash
	./run.sh
	```

This will:
- Set up environment variables for the codebase and example projects
- Build the Docker images using `docker-compose`
- Start a shell inside the `python-app` container

### What Happens Next?

- You will be dropped into a bash shell inside the container.
- From here, you can run analysis scripts, test code, or explore the environment.

### Environment Variables

- `CODEBASEAI_DIR`: Path to the main codebaseai directory
- `PROJECT_DIR`: Path to the example Python project
- `JAVA_PROJECT_DIR`: Path to the example Java project

### Troubleshooting

- If you encounter permission errors, ensure Docker is running and you have access rights.
- If you need to rebuild the images, run:
  ```bash
  cd docker
  docker-compose build --no-cache
  ```
