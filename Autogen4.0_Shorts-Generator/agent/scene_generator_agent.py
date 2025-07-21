from dotenv import load_dotenv
from openai import OpenAI
from autogen_agentchat.agents import AssistantAgent




# def image_tool(scene_description,OPENAI_API_KEY):
#     """
#     This function generates an image based on the scene description using the dalle model
#     """
#     client = OpenAI(api_key=OPENAI_API_KEY)
#     response = client.images.generate(
#                 model="dall-e-3",  # "dall-e-2" or "dall-e-3"
#                 prompt=scene_description,
#                 n=1,
#                 size='1024x1024',
#             )
#     return response.data[0].url



# def getSceneGenerator_agent():
   
#     scene_generator_prompt = """
#         You are an expert scene image generator for comedy cartoons shorts. Your task is to generate visual images based on the scriptwritter agent.
        
#         Your mission is to generate and 3 images based on the scriptwriter's input which is prsent in a list.

#         after generating the images, print TERMINATE at the end.
#         """
    
#     response = AssistantAgent(
#         name="SceneGeneratorAgent",
#         description="Generates cartoon scene images from prompts.",
#         tools=[image_tool],
#         system_message=scene_generator_prompt,
#     )
#     return response

# from autogen_agentchat.agents import AssistantAgent

def getSceneGenerator_agent(OPENAI_API_KEY,model_client):
    def image_tool(prompt:str)->str:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.images.generate(
            model="dall-e-3",  # or "dall-e-2"
            prompt=prompt,
            n=1,
            size='1024x1024',
        )
        return response.data[0].url

    return AssistantAgent(
        name="SceneGeneratorAgent",
        description="Generates cartoon scene images from prompts.",
        tools=[image_tool],
        model_client=model_client,
    )
   
   