from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor

from config.constants import TIMEOUT_DOCKER, WORK_DIR_DOCKER



def getDockerCommandLineCodeExecutor():
    docker = DockerCommandLineCodeExecutor(
        timeout = TIMEOUT_DOCKER,
        work_dir = WORK_DIR_DOCKER
    )
    return docker


async def start_docker_container(docker):
    print("Starting Docker container...")
    await docker.start()
    print('Docker container started successfully.')
    

async def stop_docker_container(docker):
    print("Stooping Docker Container...")
    await docker.stop()
    print('Docker container stopped successfully.')

   