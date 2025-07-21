from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from agents.prompts.Code_executor_agent import getCodeExecutorAgent
from agents.prompts.Data_Analyser_agent import getDataAnalyserAgent


def getAnalyzerGPTTeam(docker,model_client):
    code_executor_agent = getCodeExecutorAgent(docker)

    data_analyser_Agent = getDataAnalyserAgent(model_client)

    termination_condition = TextMentionTermination(
                    text = 'STOP',
                    sources='user'
        )
    
    team = RoundRobinGroupChat(
                    participants = [data_analyser_Agent, code_executor_agent],
                    max_turns = 10,
                    termination_condition=termination_condition,
        )
    return team
