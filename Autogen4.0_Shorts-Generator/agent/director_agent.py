from autogen_agentchat.agents import AssistantAgent



def getDirector_agent(model_client):

    director_prompt = """

    You are expect director of cartoon funny shorts visualizer. you're task is to visualize a 3-scene comedy cartoon shorts story.
    
    Your mission is to  Coordinate with 'Scriptwriter' to inform about the visualization of comedy scenes.

    For Example: A simple story premise (e.g., "Tom and Jerry fighting for cheesecake").
    
    """

    director_agent = AssistantAgent(
        name = "director_agent",
        description='You are a director of cartoon funny shorts visualizer. Your task is to visualize a 3-scene comedy cartoon shorts story.',
        model_client = model_client,
        system_message=director_prompt,
    )

    return director_agent
