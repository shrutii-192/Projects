
from langgraph.graph import MessagesState, StateGraph, END, START
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from wether_tool import Weathertool
from calculator_tool import Addition,Divide,Multiply,Percentage,calculate_discount,final_price_after_discount
from search_attraction_tool import search_Activities_tool,search_restaurant_tool,search_cafees_tool,search_attraction_tool,search_transportation_tool
import os

# openai model return
def get_openai():
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    openai_model = ChatOpenAI(api_key=OPENAI_API_KEY,model = "gpt-4.1-mini")
    return openai_model

# groq model return
def get_groq():
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    groq_model = ChatGroq(api_key = GROQ_API_KEY,model = "llama-3-8b-instruct")
    return groq_model

def tools_list():
    tools = [Weathertool,Addition,search_attraction_tool,search_restaurant_tool,search_cafees_tool,search_Activities_tool,search_transportation_tool,final_price_after_discount,Divide,Multiply,Percentage,calculate_discount,final_price_after_discount]
    return tools


# identify tool calling
def llm_decision_call(state:MessagesState):
    user_question = state["messages"]
    Decision_prompt_template ="""You are an AI Travel Planner and Expense Manager. Your task is to assist users in planning trips to any city worldwide using reasoning and tools.

                        You follow the **ReAct pattern**:
                        1. Think about what the user needs.
                        2. Decide which tool to use and why.
                        3. Call the tool using the correct arguments.
                        4. Observe the result.
                        5. Repeat reasoning and tool usage as needed.
                        6. Finally, return a complete, friendly, and well-organized travel plan.
                        7. Try Use the provided tools before trying for generic web_search tool

                        Be thoughtful and structured. Use tools only when required. Wait for tool results before deciding the next step.

                        If the user provides a destination and number of days, start by gathering key information like attractions, weather, and hotels. Calculate costs, convert currency, generate an itinerary, and end with a trip summary.
                        Correctly calcuate the trip days and use it for Estimating the cost Always get current coversion rate of the currency  and covert appropriatly . check the local weather during the time.Add a plan to visit nearby attractions.
                        Do not make any assumption
                        Your final response must be complete and organized, using markdown formatting (headers, bullet points) for easy reading. You should never hallucinate data — always use tools to get real-time or accurate info.

                        Let's get started."""
    # 
    # 
    #  """ You are a travel assistant. Based on the user’s request, decide whether to:
    #                                 - Use 'search_attraction_tool'- for questions about famous landmarks, top sights, or rated places to visit. list them with star ratings and a one-line description
    #                                 - Use 'search_Activities_tool'- for things to do, entertainment, outdoor experiences, sports, or events. list all activities along with information of each activities such as name of activity,
    #                                   category of activity,distance of the activity area from your city location. suggest only top 10 results.
    #                                 - Use 'search_restaurant_tool'/'search_cafees_tool'-for question related restaurant- or cafe tool should list them with name, address, cuisins, address
    #                                   of restaurant, opening and closing hours diet each restaurant serve(eg. vegeterian, non-vegiterian) and suggest only top 10 restaurants only. 
    #                                 - Use 'weather tool'- for weather-related queries.
    #                                 - Use 'search_flights'- tool help you to search flight along with its price from original location to destination location
    #                                 - Use 'Addition,multiplication,divide,percentage,discount,finalprice'- use to perfr arithmatic operations.
    #                                 Only call one tool at a time based on user intent.
    #                                 on the basis of user question suggest the itineary plane includes information about most attractive places, famous activities
    #                                 top restaurants its wether condition, help use to search flight etc. 

    #                            """
    SYSTEM_PROMPT = PromptTemplate(template = Decision_prompt_template)
    tools = tools_list()
    model = get_openai()
    
    format_prompt = SYSTEM_PROMPT.format()

    input_question = [SystemMessage(content = format_prompt)] + user_question
    llm_with_tools = model.bind_tools(tools)
    response = llm_with_tools.invoke(input_question)
    return {"messages":[response]}



