import asyncio
import os
from temporalio.client import Client
from temporalio.worker import Worker
from temporalio.contrib.pydantic import pydantic_data_converter
from langgraph_temporal.activities_agents.agent import data_analysis_agent
from langgraph_temporal.workflows.workflow import data_analysis_workflow


async def main():
    client = await Client.connect(
        os.getenv("TEMPORAL_ADDRESS", "localhost:7233"),
        data_converter=pydantic_data_converter,
    )
    worker = Worker(
        client,
        task_queue="langgraph",
        workflows=[data_analysis_workflow],
        activities=[data_analysis_agent],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
