from langgraph_temporal.activities_agents.prompts import SUMMARIZE_PROMPT, REPORT_PROMPT
from typing import Any, Dict
from langgraph_temporal.models import llm_client
from langchain.tools import tool


llm = llm_client()

@tool
def summarizer(data: list) -> str:
    """Summarize the given data using a language model.

    Args:
        data (list): The list of data to be summarized.

    Returns:
        str: The summary of the data.
    """
    print("Data to summarize:", data)
    prompt = SUMMARIZE_PROMPT.format(report=data)
    response = llm.invoke(prompt)
    return response.content

@tool
def reporter(data: list) -> str:
    """Generate a comprehensive report from the given JSON data using a language model.

    Args:
        data (list): The list of data to generate the report from.

    Returns:
        str: The generated report.
    """
    print("JSON data to generate report from:", data)
    prompt = REPORT_PROMPT.format(json_data=data)
    response = llm.invoke(prompt)
    return response.content