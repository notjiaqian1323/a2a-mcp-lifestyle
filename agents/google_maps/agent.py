from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import MCPToolset, StreamableHTTPConnectionParams

# 1. Connect THIS agent to the Google Maps MCP Server (The Hands)
google_maps_mcp = MCPToolset(
    connection_params=StreamableHTTPConnectionParams(
        url='http://mcp-server-google-maps:9002/mcp',
        timeout=60
    )
)

# 2. Give the agent its persona (The Brain)
PROMPT = """
    You are the TARUMT Campus Route Expert. Your job is to help students with directions, 
    travel times, and distances to and from the university.
    
    You have access to a Google Maps tool. Use it to calculate routes.
    Always provide the distance and estimated travel time in a friendly, conversational manner.
    If the user asks about traffic or the best way to get to campus, provide clear directions.
"""

# 3. Create the Agent
root_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='google_maps_agent',
    description='An agent that provides routing and travel time information using Google Maps.',
    instruction=PROMPT,
    tools=[google_maps_mcp], # Give it the MCP tool
)
