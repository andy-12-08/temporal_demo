from langgraph.prebuilt import create_react_agent
from langgraph_temporal.activities_agents.tools import summarizer, reporter
from langgraph_temporal.models import llm_client, AgentState
from langgraph_temporal.activities_agents.prompts import DATA_ANALYSIS_PROMPT
from temporalio import activity

# state = AgentState()

@activity.defn
async def data_analysis_agent(state: AgentState):
    
    agent = create_react_agent(
        tools=[summarizer, reporter],
        model=llm_client(),
        prompt=DATA_ANALYSIS_PROMPT,
        name="DataAnalysisAgent"
    )

    # Convert the list data to a dictionary for the agent
    response = agent.invoke({"data": state.data})
    print("Agent response:", response)
    
    # Extract tool results from the agent's response
    summary_result = ""
    report_result = ""
    
    # Extract from ToolMessage objects in the messages
    if "messages" in response:
        for message in response["messages"]:
            # Check if this is a ToolMessage (tool result)
            if hasattr(message, 'name') and hasattr(message, 'content'):
                if message.name == 'reporter':
                    report_result = message.content
                elif message.name == 'summarizer':
                    summary_result = message.content
    
    # Update state with extracted results
    state.summary = summary_result
    state.report = report_result
    
    print(f"Extracted Summary: {summary_result[:100]}...")
    print(f"Extracted Report: {report_result[:100]}...")
    
    return state

# if __name__ == "__main__":
#     state=AgentState()
#     data=[
#         {
#             "sales": [100, 150, 200, 250],
#             "expenses": [80, 120, 160, 200],
#             "months": ["January", "February", "March", "April"]
#         },
#         {
#             "sales": [300, 400, 500, 600],
#             "expenses": [250, 350, 450, 550],
#             "months": ["May", "June", "July", "August"]
#         },
#         {
#             "sales": [50, 75, 125, 175],
#             "expenses": [40, 60, 90, 130],
#             "months": ["September", "October", "November", "December"]
#         }
#     ]
#     state.data = data
#     updated_state = data_analysis_agent(state)
#     print("\n" * 2)
#     print("=" * 80)
#     print("Final Agent State:")
#     print(updated_state)
    