# CrewAI Patterns

> Stub — expand after first project using extracting-patterns (F2)

## Quick Start

```bash
pip install crewai
```

## Key Concepts

- **Agent**: role, goal, backstory — defines persona and capabilities
- **Task**: description, expected_output, agent — work unit assigned to an agent
- **Crew**: agents + tasks, sequential or hierarchical process

## Basic Example

```python
from crewai import Agent, Task, Crew

researcher = Agent(
    role="Research Analyst",
    goal="Find comprehensive information on the topic",
    backstory="You are an experienced research analyst.",
)

writer = Agent(
    role="Technical Writer",
    goal="Create clear, well-structured documentation",
    backstory="You are a skilled technical writer.",
)

research_task = Task(
    description="Research {topic} and provide key findings",
    expected_output="Structured research report",
    agent=researcher,
)

write_task = Task(
    description="Write documentation based on research findings",
    expected_output="Final documentation",
    agent=writer,
)

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    verbose=True,
)

result = crew.kickoff(inputs={"topic": "AI agents"})
```

## Process Types
- **Sequential**: tasks execute in order
- **Hierarchical**: manager agent delegates and reviews
