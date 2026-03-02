import os
import asyncio
import httpx
import googlemaps
from mcp.server.fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse

# 1. Initialize the MCP Server
mcp = FastMCP("Google-Maps-TARUMT")

# Define Host and Port for streamable-http (Matches Docker config)
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 9002))

# 2. Grab the API Key from the environment
api_key = os.getenv("GOOGLE_MAPS_API_KEY")

# 3. Initialize the Google Maps client
gmaps = googlemaps.Client(key=api_key) if api_key else None


@mcp.custom_route("/health", methods=["GET"])
async def liveness_check(request: Request) -> JSONResponse:
    """Liveness probe endpoint for health checks"""
    return JSONResponse({})


@mcp.tool()
def calculate_commute(origin: str, destination: str, mode: str = "driving") -> str:
    """
    Calculates the distance, estimated travel time, and route between two locations.
    Mode can be 'driving', 'walking', 'transit', or 'bicycling'.
    """
    if not gmaps:
        return "Error: GOOGLE_MAPS_API_KEY is missing from the environment."

    try:
        # Ask Google Maps for the directions
        directions_result = gmaps.directions(origin, destination, mode=mode)

        if not directions_result:
            return f"Could not find a route between {origin} and {destination}."

        # Extract the most important data from the JSON response
        leg = directions_result[0]['legs'][0]
        distance = leg['distance']['text']
        duration = leg['duration']['text']
        start_address = leg['start_address']
        end_address = leg['end_address']

        return (f"Route Data:\n"
                f"From: {start_address}\n"
                f"To: {end_address}\n"
                f"Distance: {distance}\n"
                f"Estimated Time ({mode}): {duration}")

    except Exception as e:
        return f"An API error occurred: {str(e)}"

# Start the server using streamable-http
def start_mcp_server():
    asyncio.run(
        mcp.run_async(
            transport="streamable-http",
            host=HOST,
            port=PORT,
        )
    )

if __name__ == "__main__":
    start_mcp_server()

