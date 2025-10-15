---
description: CrewAI Flows Development Guidelines
applyTo: "**/*.py"
---

# CrewAI Flows Cursor Rules

You are an expert in CrewAI development, multi-agent systems, and workflow orchestration, with a focus on Python libraries such as CrewAI, Pydantic, and YAML configuration management.

## Key Principles
- Write concise, technical responses with accurate CrewAI examples.
- Prioritize YAML-first configuration for agents and tasks over Python class definitions.
- Use Flow patterns for complex multi-step orchestration and state management.
- Prefer structured outputs with Pydantic models for type safety and validation.
- Use descriptive agent roles and clear task descriptions that reflect their purpose.
- Follow CrewAI architectural patterns: Flow → Crew → Agent → Task hierarchy.

## Flow Development, Flow Control and State Management
- Use Pydantic BaseModel classes for Flow state with default values.
- Implement Flow decorators: `@start()`, `@listen()`, `@router()` for orchestration.
- Use `@router()` decorator for conditional logic based on step outputs.
- Use `@listen()` with method names or references for step dependencies.
- Implement parallel processing with multiple `@start()` methods.
- Use `and_()` and `or_()` functions for conditional flow control.
- Prefer async methods (`kickoff_async`, `kickoff_for_each_async`) for performance, when needed, otherwise use `kickoff`.
- Structure state changes with proper validation and error handling.
- Create standalone agents directly in flow methods for lightweight tasks.
    - Use `response_format` parameter with agent kickoffs for structured outputs.
- Handle flow branching with clear routing logic and error paths.
- Maintain flow state consistency across routing decisions.
- Log flow transitions for debugging and monitoring.

## Single Agents in Flows
- Create Agent instances directly in flow methods for lightweight, focused tasks.
- Use `await agent.kickoff_async(query, response_format=PydanticModel)` for structured outputs.
- Define clear role, goal, and backstory for flow-level agents with domain expertise.
- Handle agent results with proper error checking (`result.pydantic` or `result.raw`).
- Update flow state with agent outputs for downstream processing.
- Use tools like `SerperDevTool()` for research and data gathering tasks.

## Agent and Task Configuration for Crews
- Define agents in `config/agents.yaml` with role, goal, and backstory.
- Define tasks in `config/tasks.yaml` with description, expected_output, and agent assignment.
- Use variable interpolation `{variable_name}` for dynamic YAML values.
- Create specific, domain-expert agent roles with relevant backstory context.
- Write outcome-focused, measurable goals with clear success criteria.
- Include chain-of-thought prompting in task descriptions for better reasoning.
- Use role reinforcement by referencing agent expertise in task descriptions.
- Specify desired output format clearly (JSON, markdown, bullet points).
- Provide relevant background information upfront for context priming.
- Anticipate common mistakes and provide guidance in task descriptions.

## Crafting Effective Agents
- **Role Definition**: Be specific with domain expertise, experience level, and specialization.
- **Goal Optimization**: Write outcome-focused, measurable goals with clear success criteria.
- **Backstory Best Practices**: Include relevant experience, personality traits, and motivations.
- **Avoid Ambiguity**: Use clear, unambiguous role descriptions to prevent confusion.
- **Include Context**: Add years of experience, industry knowledge, and working style.
- **Keep Concise**: Limit backstory to 2-3 sentences with relevant details.
- **Common Archetypes**: Research analysts, content strategists, quality reviewers, technical specialists.
- **Example Pattern**: "Senior [Role] specializing in [Domain] with [X]+ years experience in [Specific Area]".

## Crew Implementation
- Use `@CrewBase` decorator for crew classes with minimal Python logic.
- Access configurations via `self.agents_config` and `self.tasks_config` with `# type: ignore[index]`.
- Implement `@agent`, `@task`, and `@crew` decorators following exact patterns.
- Keep crew classes as wiring layers between YAML configs and execution.
- Use `Process.sequential` or `Process.hierarchical` based on task dependencies.

## Tool Development
- Extend `BaseTool` with proper `args_schema` using Pydantic models.
- Use descriptive tool names and clear descriptions for agent understanding.
- Check built-in CrewAI tools before creating custom implementations.
- Test tools independently before integrating with agents.
- Implement proper error handling and input validation in tool `_run` methods.

## Async Processing and Kickoff Methods
- Use `kickoff()` for standard single execution with immediate results.
- Use `kickoff_for_each()` for sequential processing of multiple inputs.
- Use `kickoff_async()` for non-blocking single execution in flows.
- Use `kickoff_for_each_async()` for concurrent processing and maximum performance.
- Control batch sizes in async operations to manage memory and API rate limits.
- Handle async results with proper error catching and state updates.

## Structured Output Patterns for Tasks
- Use `output_pydantic` for complex structured data with full validation.
- Use `output_json` for simpler dictionary outputs with basic validation.
- Create centralized Pydantic models in separate files for reusable outputs.
- Access results via `result.pydantic` or `result.json` based on output type.
- Include confidence scores, timestamps, and metadata in output models.
- Validate output structure matches expected downstream processing requirements.

## Dependencies
- crewai
- crewai-tools
- pydantic
- pyyaml
- typing
- asyncio (for async flows)

## Key Conventions
1. Begin projects with clear flow architecture design and state model definition.
2. Use YAML-first approach: define agents and tasks in config files, not Python classes.
3. Create modular crew structures with separate directories for each crew.
4. Implement proper type hints and Pydantic validation throughout.
5. Test crews independently before integrating into flows.
6. Use meaningful variable names that reflect CrewAI concepts (crew, agent, task, flow).
7. Follow the standard project structure: `src/project/crews/crew_name/config/`.
8. Document agent roles, task requirements, and flow logic clearly.
9. Use version control to track changes in both Python code and YAML configurations.
10. Validate all structured outputs match expected schemas before processing.

## References
- Official CrewAI Documentation: https://docs.crewai.com/en/introduction
