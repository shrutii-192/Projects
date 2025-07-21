from autogen_ext.models.openai import OpenAIChatCompletionClient

from config.constants import MODEL_OPENAI


import os

from dotenv import load_dotenv

load_dotenv(dotenv_path=r'E:\GENERTIVE AI\Autogen\.env')


def get_openai_model_client():
    openai_model_client = OpenAIChatCompletionClient(
        model= MODEL_OPENAI,  # Use the model name from constants
        OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")  # Set your OpenAI API key here if needed
    )
    return openai_model_client