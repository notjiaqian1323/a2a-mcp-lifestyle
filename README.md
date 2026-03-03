
# Principles

- In development, most if not all webservers containing agent(s), or adk-web, or adk web-server, will start numbering from port 8080, for ease of local debuggability
  - From docker-compose, we might expose it on a different port externally. Check `docker-compose.yml` for the latest updated value here

# Run Everything!

Run `docker-compose up` to run everything!

For exploration of A2A and MCP, this is most suitable and learn the most, however, for simplicity purpose, I suggest to go for monolith architecture instead of this docker compose microservices architecture, for cost efficiency and staying within free tier of gemini api
