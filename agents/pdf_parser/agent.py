import os
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.mcp_tool import MCPToolset

# 1. THE FIX: Correct capitalization and correct submodule path!
from google.adk.tools.mcp_tool.mcp_session_manager import SseConnectionParams

klavis_url = os.getenv("KLAVIS_MARKITDOWN_URL", "http://mcp-server-markitdown:5000/sse")

# 2. THE FIX: Use SseConnectionParams
pdf_parser_mcp = MCPToolset(
    connection_params=SseConnectionParams(
        url=klavis_url,
        timeout=120
    )
)

PROMPT = """
    You are the TARUMT Document Parser Agent. 
    You have access to a local MarkItDown MCP tool to read documents.
    
    IMPORTANT FILE PATH RULE: 
    All user files are located in the `/workspace/` directory. 
    If a user asks you to parse "timetable.pdf", you MUST tell the MCP tool to look at exactly `/workspace/timetable.pdf`.
    
    Once the tool returns the parsed Markdown text, print the raw output into the chat so the user can verify it.
"""

root_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='pdf_parser_agent',
    description='An agent that extracts text from documents using a local MarkItDown server.',
    instruction=PROMPT,
    tools=[pdf_parser_mcp],
)
