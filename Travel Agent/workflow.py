from langgraph.graph import StateGraph, MessagesState, START, END
from llmhelper import llm_decision_call,tools_list
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from IPython.display import Image, display
from langchain_core.messages import HumanMessage, SystemMessage


def Workflow_define():
    builder = StateGraph(MessagesState)
    builder.add_node("LLM_Decision_Step",llm_decision_call)
    builder.add_node("tools",ToolNode(tools_list()))
    builder.add_edge(START,"LLM_Decision_Step")
    builder.add_conditional_edges("LLM_Decision_Step",
                          tools_condition)
    builder.add_edge("tools","LLM_Decision_Step")
    react_graph = builder.compile()
    # display(Image(react_graph.get_graph().draw_mermaid_png()))
    # with open("graph.png", "wb") as f:
    #     f.write(react_graph.get_graph().draw_mermaid_png())
    # print("Graph image saved as graph.png")
    return react_graph


message = [HumanMessage(content=""" I want to visit Milan, Italy from 2025-06-20 to 2025-06-22.
                         - Esitmate the cost of the trip in INR as my transcation currency 
                         - select one hotel under euros 500 which near to the city center, 
                         - please select 5 different local dinining with price range.
                         - I would like to visit 2-3 attractions per day during the stay""")]
react_graph = Workflow_define()
response= react_graph.invoke({"messages":message})


for m in response["messages"]:
    print(m.pretty_print())
