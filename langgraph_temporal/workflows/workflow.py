import asyncio
from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy

# These imports bring in non-deterministic libraries transitively (langgraph/langchain).
# They must be marked as pass-through so the workflow sandbox allows them.
with workflow.unsafe.imports_passed_through():
    from langgraph_temporal.activities_agents.agent import data_analysis_agent
    from langgraph_temporal.models import AgentState

@workflow.defn
class data_analysis_workflow:
    @workflow.run
    async def run(self, state: AgentState) -> AgentState:
        # Define retry policy locally and pass directly to execute_activity
        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=2),
            maximum_interval=timedelta(seconds=10),
            backoff_coefficient=2.0,
            maximum_attempts=5,
        )

        # Call the data analysis agent activity with explicit options
        data_analysis_output_state = await workflow.execute_activity(
            data_analysis_agent,
            state,
            start_to_close_timeout=timedelta(seconds=60),
            retry_policy=retry_policy,
        )
        return data_analysis_output_state