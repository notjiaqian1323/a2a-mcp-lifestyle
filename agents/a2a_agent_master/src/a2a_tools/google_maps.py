import httpx
from uuid import uuid4
import asyncio # 1. ADD THIS IMPORT

from a2a.client import A2AClient
from a2a.types import (
    SendMessageRequest,
    MessageSendParams,
    Message,
    Role,
    Part,
    TextPart,
    TaskState,
)

from google.adk.tools import ToolContext

class GoogleMapsAgent:
    def __init__(self, agent_url: str):
        self.agent_url = agent_url

    async def invoke_google_maps_agent_via_a2a(
            self, query: str, tool_context: ToolContext
    ):


        """Send a query to the google maps agent to get travel times, distances, and routing information.

        Args:
            query: The navigation or routing query to send to the google maps agent (e.g. "How long to drive from Subang to TARUMT?")
        """
        request = SendMessageRequest(
            id=str(uuid4()),
            params=MessageSendParams(
                message=Message(
                    contextId=tool_context._invocation_context.session.id,
                    taskId=tool_context.state.get('task_id'),
                    messageId=str(uuid4()),
                    role=Role.user,
                    parts=[Part(TextPart(text=query))],
                )
            ),
        )

        self._update_status(tool_context)

        await asyncio.sleep(3)

        try:
            async with httpx.AsyncClient(timeout=60) as httpx_client:
                client = await A2AClient.get_client_from_agent_card_url(
                    httpx_client, self.agent_url
                )
                return await client.send_message(request)
        except Exception as e:
            print(f'An error occurred: {e}')

    def _update_status(self, tool_context: ToolContext):
        try:
            task_updater = tool_context._invocation_context.run_config.current_task_updater
            task_updater.update_status(
                TaskState.working,
                message=task_updater.new_agent_message(
                    [Part(TextPart(text='Waiting for Google Maps agent to calculate route...'))]
                ),
            )
        except Exception as e:
            print(f"Error updating status: {e} ; You might be using adk-web where the task updater is not available")