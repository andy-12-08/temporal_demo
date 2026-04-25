
from contextlib import asynccontextmanager
from uuid import uuid4
import os
from fastapi import FastAPI, HTTPException
import asyncio
from temporalio.client import Client
from temporalio.contrib.pydantic import pydantic_data_converter
from langgraph_temporal.models import AgentState
from langgraph_temporal.workflows.workflow import data_analysis_workflow


@asynccontextmanager
async def lifespan(app: FastAPI):
    temporal_address = os.getenv("TEMPORAL_ADDRESS", "localhost:7233")
    try:
        app.state.temporal_client = await Client.connect(
            temporal_address,
            data_converter=pydantic_data_converter,
        )
    except Exception as e:
        app.state.temporal_client = None
        print(f"Temporal connection failed: {e}")
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/run-workflow")
async def run_workflow(state: AgentState):
    if not app.state.temporal_client:
        raise HTTPException(status_code=503, detail="Temporal client not available")

    client = app.state.temporal_client
    workflow_id = f"data-analysis-{uuid4()}"
    handle = await client.start_workflow(
        data_analysis_workflow.run,
        state,
        id=workflow_id,
        task_queue="langgraph",
    )
    return {"workflow_id": handle.id}


@app.get("/workflows/{workflow_id}")
async def get_workflow_status(workflow_id: str):
    if not app.state.temporal_client:
        raise HTTPException(status_code=503, detail="Temporal client not available")

    client = app.state.temporal_client
    handle = client.get_workflow_handle(workflow_id=workflow_id)
    desc = await handle.describe()
    return {"workflow_id": workflow_id, "status": desc.status.name}


@app.get("/workflows/{workflow_id}/result")
async def get_workflow_result(workflow_id: str):
    if not app.state.temporal_client:
        raise HTTPException(status_code=503, detail="Temporal client not available")

    client = app.state.temporal_client
    handle = client.get_workflow_handle(workflow_id=workflow_id)
    try:
        result = await handle.result()
        return {"workflow_id": workflow_id, "result": result}
    except asyncio.TimeoutError:
        desc = await handle.describe()
        return {"workflow_id": workflow_id, "status": desc.status.name, "pending": True}