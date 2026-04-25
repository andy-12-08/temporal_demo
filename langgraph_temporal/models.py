import os
from langchain_openai import AzureChatOpenAI
from pydantic import BaseModel

# load environment variables from .env file
from dotenv import load_dotenv

load_dotenv()

def llm_client():
    return AzureChatOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_version=os.getenv("OPENAI_API_VERSION"),
)


class AgentState(BaseModel):
    data: list = []
    summary: str = ""
    report: str = ""