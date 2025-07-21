from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from constants import TIMEOUT_DOCKER, WORK_DIR_DOCKER


# execute docker commands
def getDockerCommandLineCodeExecutor():
    docker = DockerCommandLineCodeExecutor(
            work_dir=WORK_DIR_DOCKER,
            timeout=TIMEOUT_DOCKER    
    )
    return docker


# start the docker container
async def start_docker_container(docker):
    print("Starting Docker container...")
    await docker.start()
    print('Docker container started successfully.')


# stop docker container
async def stop_docker_container(docker):
    print("Stopping Docker Container...")
    await docker.stop()
    print('Docker container stopped successfully.')