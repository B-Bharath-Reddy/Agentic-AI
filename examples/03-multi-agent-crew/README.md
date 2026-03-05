# Multi-Agent Examples

This directory contains examples of multi-agent systems using different frameworks.

## Files

| File | Framework | Description |
|------|-----------|-------------|
| `crewai_example.py` | CrewAI | Research team with Researcher, Writer, Editor |
| `autogen_example.py` | AutoGen | Multi-agent chat with various patterns |

## CrewAI Example

CrewAI provides a simple way to create teams of agents that work together.

### Installation

```bash
pip install crewai crewai-tools
```

### Key Concepts

- **Agent**: An AI agent with a role, goal, and backstory
- **Task**: A specific task for an agent to complete
- **Crew**: A team of agents working together
- **Process**: How agents collaborate (sequential or hierarchical)

### Communication Patterns

```
Sequential Process:
+------------+     +------------+     +------------+
| Researcher | --> |   Writer   | --> |   Editor   |
+------------+     +------------+     +------------+

Hierarchical Process:
        +------------+
        |   Manager  |
        +------------+
              |
    +---------+---------+
    |         |         |
    v         v         v
+--------+ +--------+ +--------+
|Agent 1 | |Agent 2 | |Agent 3 |
+--------+ +--------+ +--------+
```

### Usage

```python
from crewai import Agent, Task, Crew, Process

# Create agents
researcher = Agent(
    role="Researcher",
    goal="Find information",
    backstory="Expert researcher"
)

writer = Agent(
    role="Writer", 
    goal="Write content",
    backstory="Skilled writer"
)

# Create tasks
research_task = Task(
    description="Research topic X",
    agent=researcher
)

write_task = Task(
    description="Write article about X",
    agent=writer
)

# Create and run crew
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential
)

result = crew.kickoff()
```

## AutoGen Example

Microsoft AutoGen provides flexible multi-agent conversation patterns.

### Installation

```bash
pip install pyautogen
```

### Key Concepts

- **AssistantAgent**: AI-powered agent
- **UserProxyAgent**: Represents human user
- **GroupChat**: Multi-agent conversation
- **GroupChatManager**: Coordinates group chat

### Communication Patterns

```
Two-Agent Chat:
+--------+     +-----------+
|  User  | <-> | Assistant |
+--------+     +-----------+

Group Chat:
+--------+
|  User  |
+--------+
    |
    v
+-------------------+
| GroupChatManager  |
+-------------------+
    |
    +----+----+----+
    |    |    |    |
    v    v    v    v
  Agent Agent Agent Agent

Hierarchical:
+--------+
| Manager|
+--------+
    |
    +----+----+
    |    |    |
    v    v    v
 Worker Worker Worker
```

### Usage

```python
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

# Create agents
assistant = AssistantAgent(
    name="Assistant",
    system_message="You are a helpful assistant."
)

user = UserProxyAgent(
    name="User",
    human_input_mode="NEVER"
)

# Start conversation
user.initiate_chat(
    assistant,
    message="Hello!"
)
```

## Comparison

| Feature | CrewAI | AutoGen |
|---------|--------|---------|
| Learning Curve | Low | Medium |
| Code Execution | Limited | Built-in |
| Human-in-loop | Limited | Strong |
| Customization | Medium | High |
| Production Ready | Yes | Beta |

## When to Use Which

### Use CrewAI when:
- You want a simple, opinionated framework
- Building content creation pipelines
- Need quick prototyping

### Use AutoGen when:
- You need code execution capabilities
- Want more control over conversation flow
- Building research or analysis tools
- Need human-in-the-loop

## Environment Variables

```bash
# Required for both
export OPENAI_API_KEY="your-key-here"

# Optional for CrewAI web search
export SERPER_API_KEY="your-serper-key"
```

## Further Reading

- [CrewAI Documentation](https://docs.crewai.com/)
- [AutoGen Documentation](https://microsoft.github.io/autogen/)
- [LangGraph for Multi-Agent](https://langchain-ai.github.io/langgraph/)