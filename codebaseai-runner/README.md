## How to Run `run.sh` and Use Docker Compose

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
- Export your user and group ID for file ownership in the container
- Build the Docker images using `docker-compose`
- Start a bash shell inside the `python-app` container

### Environment Variables

- `CODEBASEAI_DIR`: Path to the main codebaseai directory
- `PROJECT_DIR`: Path to the example Python project
- `JAVA_PROJECT_DIR`: Path to the example Java project
- `UID` and `GID`: Your user and group ID, passed to Docker for correct file ownership

### Keeping the Container Running

- By default, `run.sh` starts an interactive shell. If you want the container to run in the background, set the Dockerfile `CMD` to:
	```dockerfile
	CMD ["tail", "-f", "/dev/null"]
	```
- Or use `docker-compose up -d` and then `docker-compose exec python-app bash` to enter the running container.

### Troubleshooting

- If you encounter permission errors, ensure Docker is running and you have access rights.
- If files are created as `root`, make sure your Docker Compose and Dockerfile use your UID/GID:
	```yaml
	services:
		python-app:
			user: "${UID}:${GID}"
	```
- If you need to rebuild the images, run:
	```bash
	cd docker
	docker-compose build --no-cache
	```


### Notes

- All files created in mounted volumes will be owned by your user if UID/GID is set correctly.
