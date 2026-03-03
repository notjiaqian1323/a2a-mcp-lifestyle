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

class PdfParserAgent:
    def __init__(self, agent_url: str):
        self.agent_url = agent_url

    async def invoke_pdf_parser_agent_via_a2a(
            self, document_query: str, tool_context: ToolContext
    ):
        """Send a document URL or parsing request to the PDF Parser Agent.

        Args:
            document_query: The request containing the URL of the document/PDF to be parsed (e.g., "Parse this timetable at https://...")
        """
        request = SendMessageRequest(
            id=str(uuid4()),
            params=MessageSendParams(
                message=Message(
                    contextId=tool_context._invocation_context.session.id,
                    taskId=tool_context.state.get('task_id'),
                    messageId=str(uuid4()),
                    role=Role.user,
                    parts=[Part(TextPart(text=document_query))],
                )
            ),
        )

        self._update_status(tool_context)

        print("Throttling request for 15 seconds to prevent API Rate Limiting...")
        await asyncio.sleep(15)

        try:
            # 3. Increase the timeout to 120 seconds so the connection doesn't drop while we are sleeping!
            async with httpx.AsyncClient(timeout=120) as httpx_client:
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
                    [Part(TextPart(text='Waiting for PDF Parser Agent to read the document...'))]
                ),
            )
        except Exception as e:
            print(f"Error updating status: {e} ; You might be using adk-web where the task updater is not available")