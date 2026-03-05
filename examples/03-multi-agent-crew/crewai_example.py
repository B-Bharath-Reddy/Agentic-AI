"""
CrewAI Multi-Agent Example
==========================
Demonstrates how to build a multi-agent system using CrewAI.

This example creates a research team with three agents:
1. Researcher - Gathers information
2. Writer - Creates content
3. Editor - Reviews and improves

Installation:
    pip install crewai crewai-tools

Usage:
    python crewai_example.py
"""

import os
from typing import Optional

# Check for required packages
try:
    from crewai import Agent, Task, Crew, Process
    from crewai_tools import SerperDevTool, WebsiteSearchTool
    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False
    print("CrewAI not installed. Install with: pip install crewai crewai-tools")


# ============================================================================
# TOOLS CONFIGURATION
# ============================================================================

def get_tools():
    """Get available tools for the agents."""
    tools = []
    
    # Web search tool (requires SERPER_API_KEY)
    if os.getenv("SERPER_API_KEY"):
        try:
            search_tool = SerperDevTool()
            tools.append(search_tool)
        except Exception as e:
            print(f"Could not initialize SerperDevTool: {e}")
    
    # Website search tool
    try:
        website_tool = WebsiteSearchTool()
        tools.append(website_tool)
    except Exception as e:
        print(f"Could not initialize WebsiteSearchTool: {e}")
    
    return tools


# ============================================================================
# AGENT DEFINITIONS
# ============================================================================

def create_researcher(tools: list) -> Agent:
    """
    Create the Researcher agent.
    
    This agent is responsible for:
    - Gathering information from the web
    - Finding relevant sources
    - Summarizing research findings
    """
    return Agent(
        role="Senior Research Analyst",
        goal="Uncover cutting-edge developments in AI and data science",
        backstory="""You are a senior research analyst at a leading tech think tank.
        Your expertise lies in identifying emerging trends and technologies in AI.
        You have a knack for dissecting complex data and presenting actionable insights.
        You are known for your ability to find the most relevant information quickly.""",
        verbose=True,
        allow_delegation=False,
        tools=tools,
        llm="gpt-4o"  # Can also use "openai/gpt-4o" or other providers
    )


def create_writer() -> Agent:
    """
    Create the Writer agent.
    
    This agent is responsible for:
    - Transforming research into engaging content
    - Writing clear and compelling articles
    - Maintaining consistent tone and style
    """
    return Agent(
        role="Tech Content Strategist",
        goal="Craft compelling content on tech advancements",
        backstory="""You are a renowned content strategist specializing in tech journalism.
        You transform complex concepts into compelling narratives that resonate with audiences.
        Your articles have been featured in top tech publications.
        You excel at making technical topics accessible and engaging.""",
        verbose=True,
        allow_delegation=True,  # Can delegate to researcher for more info
        llm="gpt-4o"
    )


def create_editor() -> Agent:
    """
    Create the Editor agent.
    
    This agent is responsible for:
    - Reviewing content for quality
    - Ensuring factual accuracy
    - Improving clarity and flow
    """
    return Agent(
        role="Senior Editor",
        goal="Edit and refine content to ensure quality and accuracy",
        backstory="""You are a senior editor at a prestigious tech publication.
        You have an eye for detail and a commitment to excellence.
        You ensure all content meets the highest editorial standards.
        You are known for your constructive feedback and ability to elevate any piece.""",
        verbose=True,
        allow_delegation=False,
        llm="gpt-4o"
    )


# ============================================================================
# TASK DEFINITIONS
# ============================================================================

def create_research_task(agent: Agent, topic: str) -> Task:
    """Create a research task for the given topic."""
    return Task(
        description=f"""
        Conduct a comprehensive analysis of the latest advancements in {topic}.
        
        Focus on:
        1. Key technological breakthroughs in the past year
        2. Major industry players and their contributions
        3. Potential future implications
        4. Challenges and limitations
        
        Provide a detailed summary of your findings.
        """,
        expected_output="A comprehensive 3-paragraph research report on the topic",
        agent=agent
    )


def create_writing_task(agent: Agent, research_task: Task) -> Task:
    """Create a writing task based on research."""
    return Task(
        description="""
        Using the research findings, write an engaging blog post.
        
        Requirements:
        1. Compelling headline
        2. Introduction that hooks the reader
        3. Clear structure with subheadings
        4. Practical insights and takeaways
        5. Conclusion with future outlook
        
        The post should be informative yet accessible to a general tech audience.
        """,
        expected_output="A well-structured blog post of approximately 500 words",
        agent=agent,
        context=[research_task]  # This task depends on research_task
    )


def create_editing_task(agent: Agent, writing_task: Task) -> Task:
    """Create an editing task for the written content."""
    return Task(
        description="""
        Review and edit the blog post for:
        
        1. Clarity and readability
        2. Factual accuracy
        3. Grammar and style consistency
        4. Engaging tone
        5. Proper structure
        
        Provide the final polished version of the article.
        """,
        expected_output="A polished, publication-ready blog post",
        agent=agent,
        context=[writing_task]  # This task depends on writing_task
    )


# ============================================================================
# CREW CREATION AND EXECUTION
# ============================================================================

def create_research_crew(topic: str) -> Crew:
    """
    Create a research crew with researcher, writer, and editor agents.
    
    Args:
        topic: The topic to research and write about
        
    Returns:
        A Crew instance ready to execute
    """
    # Get tools
    tools = get_tools()
    
    # Create agents
    researcher = create_researcher(tools)
    writer = create_writer()
    editor = create_editor()
    
    # Create tasks
    research_task = create_research_task(researcher, topic)
    writing_task = create_writing_task(writer, research_task)
    editing_task = create_editing_task(editor, writing_task)
    
    # Create crew with sequential process
    crew = Crew(
        agents=[researcher, writer, editor],
        tasks=[research_task, writing_task, editing_task],
        process=Process.sequential,  # Tasks execute in order
        verbose=True
    )
    
    return crew


def run_research_pipeline(topic: str) -> str:
    """
    Run the complete research pipeline.
    
    Args:
        topic: The topic to research
        
    Returns:
        The final edited article
    """
    if not CREWAI_AVAILABLE:
        return "CrewAI not installed. Please install with: pip install crewai crewai-tools"
    
    print(f"\n{'='*60}")
    print(f"Starting Research Pipeline: {topic}")
    print(f"{'='*60}\n")
    
    crew = create_research_crew(topic)
    result = crew.kickoff()
    
    print(f"\n{'='*60}")
    print("FINAL OUTPUT")
    print(f"{'='*60}\n")
    print(result)
    
    return result


# ============================================================================
# HIERARCHICAL PROCESS EXAMPLE
# ============================================================================

def create_hierarchical_crew(topic: str) -> Crew:
    """
    Create a crew with hierarchical process (manager agent).
    
    In this mode, a manager agent coordinates the work.
    """
    tools = get_tools()
    
    # Create agents (no need to specify tasks - manager will delegate)
    researcher = Agent(
        role="Researcher",
        goal="Find information on given topics",
        backstory="Expert researcher with web search capabilities",
        tools=tools,
        llm="gpt-4o"
    )
    
    writer = Agent(
        role="Writer",
        goal="Write engaging content",
        backstory="Skilled tech writer",
        llm="gpt-4o"
    )
    
    # Create crew with hierarchical process
    crew = Crew(
        agents=[researcher, writer],
        tasks=[],  # Tasks will be created by manager
        process=Process.hierarchical,
        manager_llm="gpt-4o",  # LLM for the manager
        verbose=True
    )
    
    return crew


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Check for API keys
    if not os.getenv("OPENAI_API_KEY"):
        print("WARNING: OPENAI_API_KEY not set.")
        print("Set it with: export OPENAI_API_KEY='your-key-here'")
        print("\nRunning in demo mode...\n")
    
    # Example topic
    TOPIC = "Agentic AI and Autonomous Systems"
    
    if CREWAI_AVAILABLE:
        # Run the sequential pipeline
        result = run_research_pipeline(TOPIC)
    else:
        # Show structure when CrewAI is not installed
        print("\n" + "="*60)
        print("MULTI-AGENT CREW STRUCTURE (CrewAI)")
        print("="*60)
        print("""
    +-------------------+     +-------------------+     +-------------------+
    |    RESEARCHER     | --> |      WRITER       | --> |      EDITOR       |
    +-------------------+     +-------------------+     +-------------------+
            |                         |                         |
            v                         v                         v
    - Web search              - Transform research      - Review content
    - Gather info               into content             - Check accuracy
    - Summarize               - Write article           - Improve clarity
                                                     - Final polish
        """)
        
        print("\nCOMMUNICATION PATTERNS:")
        print("""
    Sequential Process:
    Researcher -> Writer -> Editor (fixed order)
    
    Hierarchical Process:
    Manager coordinates all agents dynamically
        """)
        
        print("\nINSTALLATION:")
        print("    pip install crewai crewai-tools")
        print("\nREQUIRED ENVIRONMENT VARIABLES:")
        print("    OPENAI_API_KEY - For LLM calls")
        print("    SERPER_API_KEY - For web search (optional)")