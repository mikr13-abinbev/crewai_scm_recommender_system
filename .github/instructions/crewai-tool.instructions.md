---
description: CrewAI Tools and MCP Integration Rules to decide when use crewai tools within crews, when and how to build custom tools or how to use MCP servers
applyTo: "**/tools/*.py"
---

# CrewAI Tools and MCP Integration Cursor Rules

You are an expert in CrewAI tools architecture, custom tool development, and Model Context Protocol (MCP) integration.

## Key Principles
- Prioritize built-in CrewAI tools over custom implementations when available
- Always ask about MCP availability before implementing custom tools
- Use type-safe tool development with Pydantic schemas
- Implement comprehensive error handling and validation
- Document tool purpose, usage, and requirements clearly

## Tool Selection Priority
1. **Built-in CrewAI Tools**: Research available tools at https://docs.crewai.com/en/tools/overview
2. **MCP Tools**: Check for community MCP implementations
3. **Custom Tools**: Create only when no alternatives exist
4. **Always Ask**: When multiple options exist, ask user preference

## Built-in Tools Reference
For comprehensive list of 40+ built-in tools, research the official documentation:
- **Tools Overview**: https://docs.crewai.com/en/tools/overview
- **Categories**: File operations, Web scraping, Database, Cloud, AI/ML integration
- **Examples**: `SerperDevTool()`, `ScrapeWebsiteTool()`, `FileReadTool()`, `PGSearchTool()`

## Custom Tool Development

### Method 1: BaseTool Subclassing (Recommended)
```python
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Any, Optional
import requests

class APISearchInput(BaseModel):
    """Input schema for API search tool."""
    query: str = Field(..., description="Search query to execute")
    limit: int = Field(default=10, description="Maximum results to return")
    category: Optional[str] = Field(None, description="Category filter")

class APISearchTool(BaseTool):
    name: str = "API Search Tool"
    description: str = (
        "Searches external API for information based on query. "
        "Use this when you need to find specific data from our external systems."
    )
    args_schema: Type[BaseModel] = APISearchInput

    def _run(self, query: str, limit: int = 10, category: Optional[str] = None) -> str:
        """Execute the search operation."""
        try:
            # Build API request
            params = {"q": query, "limit": limit}
            if category:
                params["category"] = category

            # Make API call
            response = requests.get("https://api.example.com/search", params=params)
            response.raise_for_status()

            # Process results
            data = response.json()
            results = data.get("results", [])

            if not results:
                return f"No results found for query: {query}"

            # Format output
            formatted_results = []
            for item in results[:limit]:
                formatted_results.append(f"- {item.get('title', 'N/A')}: {item.get('description', 'N/A')}")

            return f"Found {len(results)} results:\n" + "\n".join(formatted_results)

        except requests.RequestException as e:
            return f"API request failed: {str(e)}"
        except Exception as e:
            return f"Tool execution error: {str(e)}"
```

### Advanced Tool Features

#### Caching Implementation
```python
from functools import lru_cache
import hashlib
import json

class CachedAPITool(BaseTool):
    name: str = "Cached API Tool"
    description: str = "API tool with intelligent caching"
    args_schema: Type[BaseModel] = APISearchInput

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._cache = {}

    def _generate_cache_key(self, query: str, **kwargs) -> str:
        """Generate cache key from parameters."""
        cache_data = {"query": query, **kwargs}
        cache_string = json.dumps(cache_data, sort_keys=True)
        return hashlib.md5(cache_string.encode()).hexdigest()

    def _run(self, query: str, **kwargs) -> str:
        # Check cache first
        cache_key = self._generate_cache_key(query, **kwargs)
        if cache_key in self._cache:
            return f"[CACHED] {self._cache[cache_key]}"

        # Execute API call
        result = self._execute_api_call(query, **kwargs)

        # Store in cache
        self._cache[cache_key] = result
        return result

    def _execute_api_call(self, query: str, **kwargs) -> str:
        # Actual API implementation
        pass
```

#### Rate Limiting
```python
import time
from collections import defaultdict

class RateLimitedTool(BaseTool):
    name: str = "Rate Limited Tool"
    description: str = "Tool with built-in rate limiting"

    def __init__(self, max_calls_per_minute: int = 60, **kwargs):
        super().__init__(**kwargs)
        self.max_calls_per_minute = max_calls_per_minute
        self.call_timestamps = defaultdict(list)

    def _check_rate_limit(self) -> bool:
        """Check if we're within rate limits."""
        now = time.time()
        minute_ago = now - 60

        # Clean old timestamps
        self.call_timestamps["default"] = [
            ts for ts in self.call_timestamps["default"]
            if ts > minute_ago
        ]

        # Check limit
        if len(self.call_timestamps["default"]) >= self.max_calls_per_minute:
            return False

        # Record this call
        self.call_timestamps["default"].append(now)
        return True

    def _run(self, **kwargs) -> str:
        if not self._check_rate_limit():
            return "Rate limit exceeded. Please wait before making more requests."

        # Execute tool logic
        return "Tool executed successfully"
```

## MCP (Model Context Protocol) Integration

### MCP Server Configuration
```python
import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.types import StdioServerParameters

@CrewBase
class MCPEnabledCrew:
    """Crew with comprehensive MCP server integration."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # Priority order: SSE > HTTPS > StdIO
    mcp_server_params = [
        # SSE Server (Preferred)
        {
            "url": "http://localhost:8000/sse",
            "transport": "sse"
        },
        # Streamable HTTP Server (Secondary)
        {
            "url": "http://localhost:8001/mcp",
            "transport": "streamable-http"
        },
        # StdIO Server (Fallback)
        StdioServerParameters(
            command="python3",
            args=["servers/custom_mcp_server.py"],
            env={"UV_PYTHON": "3.12", **os.environ},
        )
    ]

    @agent
    def mcp_research_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["mcp_research_agent"],
            tools=self.get_mcp_tools(),  # Automatically get all MCP tools
            verbose=True,
        )

    @agent
    def hybrid_agent(self) -> Agent:
        """Agent using both built-in and MCP tools."""
        builtin_tools = [
            SerperDevTool(),
            FileWriteTool(),
        ]
        mcp_tools = self.get_mcp_tools()

        return Agent(
            config=self.agents_config["hybrid_agent"],
            tools=builtin_tools + mcp_tools,
            verbose=True,
        )

    @task
    def mcp_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config["mcp_analysis_task"],
            agent=self.mcp_research_agent(),
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential
        )
```

### MCP Best Practices
- **Transport Priority**: Always prefer SSE or HTTPS over StdIO for production
- **Tool Discovery**: Use `self.get_mcp_tools()` to automatically discover available tools
- **Error Handling**: Implement fallbacks when MCP servers are unavailable
- **Environment Setup**: Ensure proper Python environment for StdIO servers
- **Testing**: Test MCP connectivity before deploying crews

## Tool Usage in Agents
```python
@agent
def hybrid_agent(self) -> Agent:
    """Agent using both built-in and MCP tools."""
    builtin_tools = [
        SerperDevTool(),        # Research built-in tools at docs.crewai.com
        FileWriteTool(),
    ]
    mcp_tools = self.get_mcp_tools()  # Get all available MCP tools

    return Agent(
        config=self.agents_config["hybrid_agent"],
        tools=builtin_tools + mcp_tools,
        verbose=True,
    )
```

## Key Conventions

1. **Tool Selection**: Always ask about MCP availability before custom implementation
2. **Research First**: Check CrewAI docs for built-in tools before creating custom ones
3. **Error Handling**: Implement comprehensive try-catch with user-friendly messages
4. **Validation**: Use Pydantic schemas for all tool inputs
5. **Transport Priority**: HTTPS > SSE > StdIO for MCP servers
6. **Documentation**: Clear descriptions for agent understanding

## References

- CrewAI Tools Overview: https://docs.crewai.com/en/tools/overview
- Custom Tools Guide: https://docs.crewai.com/en/learn/create-custom-tools
