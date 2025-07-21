from autogen_agentchat.teams import RoundRobinGroupChat
from agent.director_agent import getDirector_agent
from agent.scriptwriter_agent import getScriptWriter_agent
from agent.scriptreviewer_agent import getScripReviewer_agent
from agent.scene_generator_agent import getSceneGenerator_agent
from autogen_agentchat.conditions import TextMentionTermination
from dotenv import load_dotenv


def short_generator_team(model_client,OPENAI_API_KEY):
    

    director_agent = getDirector_agent(model_client)
    script_writer_agent = getScriptWriter_agent(model_client)
    script_reviewer_agent = getScripReviewer_agent()
    scene_generator_agent = getSceneGenerator_agent(OPENAI_API_KEY,model_client)

    print("director_agent:", type(director_agent), director_agent)
    print("script_writer_agent:", type(script_writer_agent), script_writer_agent)
    print("script_reviewer_agent:", type(script_reviewer_agent), script_reviewer_agent)
    print("scene_generator_agent:", type(scene_generator_agent), scene_generator_agent)

    termination_condition = TextMentionTermination(
                    text = 'STOP',
                    sources='user'
        )
    team = RoundRobinGroupChat(
        participants = [director_agent, script_writer_agent, script_reviewer_agent,scene_generator_agent],
        max_turns = 6,
        termination_condition=termination_condition
    )
    return team

