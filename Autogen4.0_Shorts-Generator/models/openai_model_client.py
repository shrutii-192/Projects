from autogen_ext.models.openai import OpenAIChatCompletionClient
import os
from dotenv import load_dotenv
# from config.constants import MODEL_OPENAI




def get_openai_model_client(OPENAI_API_KEY):
    openai_model_client = OpenAIChatCompletionClient(
        model = 'gpt-4.1-mini',
        OPENAI_API_KEY = OPENAI_API_KEY
    )
    return openai_model_client



