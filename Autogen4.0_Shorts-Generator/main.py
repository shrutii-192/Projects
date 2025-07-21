from autogen_agentchat.messages import TextMessage
# from config.docker_utils import getDockerCommandLineCodeExecutor, start_docker_container, stop_docker_container
from models.openai_model_client import get_openai_model_client
from teams.movie_generator_teams import short_generator_team
from dotenv import load_dotenv
import os
import asyncio
# Load environment variables from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


async def main():

    # docker = getDockerCommandLineCodeExecutor()
    model_client = get_openai_model_client(OPENAI_API_KEY)

    team = short_generator_team(model_client, OPENAI_API_KEY)
    try:
        task = 'Can you generate a short comedy cartoon script for tom and jerry fighting on chesscake?'

        # await start_docker_container(docker)

        async for message in team.run_stream(task=task):
            print(message)
    except Exception as e:
        print(f"An error occurred: {e}")
    # finally:
        # await stop_docker_container(docker)



if __name__ == "__main__":
    asyncio.run(main())
    print("Main function completed.")

