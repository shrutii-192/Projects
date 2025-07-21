import asyncio
from config.docker_utils import getDockerCommandLineCodeExecutor, start_docker_container, stop_docker_container 
from models.openai_model_client import get_openai_model_client
from teams.analyzer_gpt import getAnalyzerGPTTeam
from autogen_agentchat.messages import TextMessage

async def main():
    openai_model_client = get_openai_model_client()
    docker = getDockerCommandLineCodeExecutor()
    

    team = getAnalyzerGPTTeam(docker, openai_model_client)
    try:
        task = 'Can you give me a graph of types of flowers in my data iris.csv'

        await start_docker_container(docker)

        async for message in team.run_stream(task=task):
            print(message)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        await stop_docker_container(docker)

if __name__ == "__main__":
    asyncio.run(main())
    print("Main function completed.")
