---
description: CrewAI Event Bus Guidelines
applyTo: "**/*.py"
---

# CrewAI Event Listeners - Practical Guide

## Overview

CrewAI provides a powerful event system that allows you to listen for and react to various events during the execution of your Crew. This enables custom integrations, monitoring, logging, and other functionality triggered by CrewAI's internal events.

## How It Works

CrewAI uses an event bus architecture with three key components:
1. **CrewAIEventsBus**: Singleton event bus managing event registration and emission
2. **BaseEvent**: Base class for all events
3. **BaseEventListener**: Abstract base class for creating custom event listeners

## Basic Example

Here's a simple example of creating a custom event listener:

```python
from crewai.events import (
    CrewKickoffStartedEvent,
    CrewKickoffCompletedEvent,
    AgentExecutionCompletedEvent,
)
from crewai.events import BaseEventListener

class MyCustomListener(BaseEventListener):
    def __init__(self):
        super().__init__()

    def setup_listeners(self, crewai_event_bus):
        @crewai_event_bus.on(CrewKickoffStartedEvent)
        def on_crew_started(source, event):
            print(f"Crew '{event.crew_name}' has started execution!")

        @crewai_event_bus.on(CrewKickoffCompletedEvent)
        def on_crew_completed(source, event):
            print(f"Crew '{event.crew_name}' has completed execution!")
            print(f"Output: {event.output}")

        @crewai_event_bus.on(AgentExecutionCompletedEvent)
        def on_agent_execution_completed(source, event):
            print(f"Agent '{event.agent.role}' completed task")
            print(f"Output: {event.output}")
```

## How to Register Your Listener

**IMPORTANT**: Just defining the listener class isn't enough. You must create an instance and import it properly.

### Option 1: In Your Crew File

```python
# In your crew.py file
from crewai import Agent, Crew, Task
from my_listeners import MyCustomListener

# Create an instance of your listener
my_listener = MyCustomListener()

class MyCustomCrew:
    def crew(self):
        return Crew(
            agents=[...],
            tasks=[...],
        )
```

### Option 2: In Your Flow File

```python
# In your main.py or flow.py file
from crewai.flow import Flow, listen, start
from my_listeners import MyCustomListener

# Create an instance of your listener
my_listener = MyCustomListener()

class MyCustomFlow(Flow):
    @start()
    def first_step(self):
        # ...
```

### Option 3: Structured Package Approach

1. Create a listeners package:
```
my_project/
  ├── listeners/
  │   ├── __init__.py
  │   ├── my_custom_listener.py
  │   └── another_listener.py
```

2. In `my_custom_listener.py`:
```python
from crewai.events import BaseEventListener
# ... import events ...

class MyCustomListener(BaseEventListener):
    # ... implementation ...

# Create an instance of your listener
my_custom_listener = MyCustomListener()
```

3. In `__init__.py`:
```python
from .my_custom_listener import my_custom_listener
from .another_listener import another_listener

__all__ = ['my_custom_listener', 'another_listener']
```

4. Import in your main file:
```python
import my_project.listeners  # This loads all your listeners

class MyCustomCrew:
    # Your crew implementation...
```

## ALL Available Event Types

### Crew Events
- **CrewKickoffStartedEvent**: When a Crew starts execution
- **CrewKickoffCompletedEvent**: When a Crew completes execution
- **CrewKickoffFailedEvent**: When a Crew fails to complete execution
- **CrewTestStartedEvent**: When a Crew starts testing
- **CrewTestCompletedEvent**: When a Crew completes testing
- **CrewTestFailedEvent**: When a Crew fails to complete testing
- **CrewTrainStartedEvent**: When a Crew starts training
- **CrewTrainCompletedEvent**: When a Crew completes training
- **CrewTrainFailedEvent**: When a Crew fails to complete training

### Agent Events
- **AgentExecutionStartedEvent**: When an Agent starts executing a task
- **AgentExecutionCompletedEvent**: When an Agent completes executing a task
- **AgentExecutionErrorEvent**: When an Agent encounters an error during execution

### Task Events
- **TaskStartedEvent**: When a Task starts execution
- **TaskCompletedEvent**: When a Task completes execution
- **TaskFailedEvent**: When a Task fails to complete execution
- **TaskEvaluationEvent**: When a Task is evaluated

### Tool Usage Events
- **ToolUsageStartedEvent**: When a tool execution is started
- **ToolUsageFinishedEvent**: When a tool execution is completed
- **ToolUsageErrorEvent**: When a tool execution encounters an error
- **ToolValidateInputErrorEvent**: When a tool input validation encounters an error
- **ToolExecutionErrorEvent**: When a tool execution encounters an error
- **ToolSelectionErrorEvent**: When there's an error selecting a tool

### Knowledge Events
- **KnowledgeRetrievalStartedEvent**: When a knowledge retrieval is started
- **KnowledgeRetrievalCompletedEvent**: When a knowledge retrieval is completed
- **KnowledgeQueryStartedEvent**: When a knowledge query is started
- **KnowledgeQueryCompletedEvent**: When a knowledge query is completed
- **KnowledgeQueryFailedEvent**: When a knowledge query fails
- **KnowledgeSearchQueryFailedEvent**: When a knowledge search query fails

### LLM Guardrail Events
- **LLMGuardrailStartedEvent**: When a guardrail validation starts (includes guardrail details and retry count)
- **LLMGuardrailCompletedEvent**: When a guardrail validation completes (includes success/failure, results, error messages)

### Flow Events
- **FlowCreatedEvent**: When a Flow is created
- **FlowStartedEvent**: When a Flow starts execution
- **FlowFinishedEvent**: When a Flow completes execution
- **FlowPlotEvent**: When a Flow is plotted
- **MethodExecutionStartedEvent**: When a Flow method starts execution
- **MethodExecutionFinishedEvent**: When a Flow method completes execution
- **MethodExecutionFailedEvent**: When a Flow method fails to complete execution

### LLM Events
- **LLMCallStartedEvent**: When an LLM call starts
- **LLMCallCompletedEvent**: When an LLM call completes
- **LLMCallFailedEvent**: When an LLM call fails
- **LLMStreamChunkEvent**: For each chunk received during streaming LLM responses

### Memory Events
- **MemoryQueryStartedEvent**: When a memory query is started (includes query, limit, score threshold)
- **MemoryQueryCompletedEvent**: When a memory query completes successfully (includes results, execution time)
- **MemoryQueryFailedEvent**: When a memory query fails (includes error message)
- **MemorySaveStartedEvent**: When a memory save operation starts (includes value, metadata, agent role)
- **MemorySaveCompletedEvent**: When a memory save operation completes (includes save execution time)
- **MemorySaveFailedEvent**: When a memory save operation fails (includes error message)
- **MemoryRetrievalStartedEvent**: When memory retrieval for a task prompt starts (includes task ID)
- **MemoryRetrievalCompletedEvent**: When memory retrieval completes (includes memory content, execution time)

## Event Handler Structure

Each event handler receives two parameters:
1. **source**: The object that emitted the event
2. **event**: The event instance with event-specific data

All events include:
- **timestamp**: When the event was emitted
- **type**: String identifier for the event type
- Additional fields vary by event type

## Advanced Usage: Scoped Handlers

For temporary event handling (testing/specific operations):

```python
from crewai.events import crewai_event_bus, CrewKickoffStartedEvent

with crewai_event_bus.scoped_handlers():
    @crewai_event_bus.on(CrewKickoffStartedEvent)
    def temp_handler(source, event):
        print("This handler only exists within this context")

    # Do something that emits events

# Outside the context, the temporary handler is removed
```

## Use Cases

1. **Logging and Monitoring**: Track execution and log important events
2. **Analytics**: Collect performance and behavior data
3. **Debugging**: Set up temporary listeners for specific issues
4. **Integration**: Connect with external systems (monitoring, databases, notifications)
5. **Custom Behavior**: Trigger custom actions based on specific events

## Best Practices

1. **Keep Handlers Light**: Event handlers should be lightweight and avoid blocking operations
2. **Error Handling**: Include proper error handling to prevent exceptions from affecting main execution
3. **Cleanup**: Ensure resources are properly cleaned up
4. **Selective Listening**: Only listen for events you actually need
5. **Testing**: Test event listeners in isolation

---

*Source: [CrewAI Event Listeners Documentation](https://docs.crewai.com/en/concepts/event-listener#event-listeners)*
