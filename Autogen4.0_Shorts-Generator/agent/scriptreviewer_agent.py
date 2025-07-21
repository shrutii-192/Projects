from autogen_agentchat.agents import UserProxyAgent


def getScripReviewer_agent():
    user_proxy_agent = UserProxyAgent(
        name = "UserProxyAgent", 
        description="A proxy for the user to approve or disapprove tasks."
        )
    return user_proxy_agent