"""
AutoGen Multi-Agent Example
===========================
Demonstrates how to build a multi-agent system using Microsoft AutoGen.

This example creates a research team with multiple agents that collaborate:
1. UserProxyAgent - Represents the human user
2. AssistantAgent - AI assistant for tasks
3. GroupChat - Enables multi-agent conversation

Installation:
    pip install pyautogen

Usage:
    python autogen_example.py
"""

import os
from typing import Optional, List, Dict

# Check for required packages
try:
    import autogen
    from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
    AUTOGEN_AVAILABLE = True
except ImportError:
    AUTOGEN_AVAILABLE = False
    print("AutoGen not installed. Install with: pip install pyautogen")


# ============================================================================
# CONFIGURATION
# ============================================================================

def get_llm_config(model: str = "gpt-4o") -> dict:
    """
    Get LLM configuration for AutoGen.
    
    Args:
        model: The model to use (default: gpt-4o)
        
    Returns:
        Configuration dictionary
    """
    return {
        "model": model,
        "api_key": os.getenv("OPENAI_API_KEY"),
        "temperature": 0.7,
        "timeout": 120,
    }


def get_config_list() -> list:
    """Get list of configurations for AutoGen."""
    return [
        {
            "model": "gpt-4o",
            "api_key": os.getenv("OPENAI_API_KEY"),
        }
    ]


# ============================================================================
# AGENT CREATION FUNCTIONS
# ============================================================================

def create_assistant_agent(
    name: str,
    system_message: str,
    llm_config: dict
) -> AssistantAgent:
    """
    Create an assistant agent.
    
    Args:
        name: Agent name
        system_message: System prompt for the agent
        llm_config: LLM configuration
        
    Returns:
        AssistantAgent instance
    """
    return AssistantAgent(
        name=name,
        system_message=system_message,
        llm_config={"config_list": [llm_config]},
    )


def create_user_proxy(
    name: str = "UserProxy",
    human_input_mode: str = "NEVER",
    max_consecutive_auto_reply: int = 10,
    code_execution_config: Optional[dict] = None
) -> UserProxyAgent:
    """
    Create a user proxy agent.
    
    Args:
        name: Agent name
        human_input_mode: "ALWAYS", "NEVER", or "TERMINATE"
        max_consecutive_auto_reply: Max auto replies
        code_execution_config: Code execution settings
        
    Returns:
        UserProxyAgent instance
    """
    if code_execution_config is None:
        code_execution_config = {
            "work_dir": "coding",
            "use_docker": False,  # Set to True for safer execution
        }
    
    return UserProxyAgent(
        name=name,
        human_input_mode=human_input_mode,
        max_consecutive_auto_reply=max_consecutive_auto_reply,
        code_execution_config=code_execution_config,
    )


# ============================================================================
# SPECIALIZED AGENTS
# ============================================================================

def create_researcher_agent(llm_config: dict) -> AssistantAgent:
    """Create a researcher agent specialized in gathering information."""
    return create_assistant_agent(
        name="Researcher",
        system_message="""You are a senior research analyst.
        
Your responsibilities:
- Gather and analyze information on given topics
- Provide comprehensive research summaries
- Identify key trends and insights
- Cite sources when possible

Always be thorough and accurate in your research.
Reply 'TERMINATE' when the task is complete.""",
        llm_config=llm_config
    )


def create_writer_agent(llm_config: dict) -> AssistantAgent:
    """Create a writer agent specialized in content creation."""
    return create_assistant_agent(
        name="Writer",
        system_message="""You are a skilled tech writer.

Your responsibilities:
- Transform research into engaging content
- Write clear and compelling articles
- Maintain consistent tone and style
- Structure content with proper headings

Focus on making complex topics accessible.
Reply 'TERMINATE' when the task is complete.""",
        llm_config=llm_config
    )


def create_editor_agent(llm_config: dict) -> AssistantAgent:
    """Create an editor agent specialized in content review."""
    return create_assistant_agent(
        name="Editor",
        system_message="""You are a senior editor at a tech publication.

Your responsibilities:
- Review content for clarity and accuracy
- Improve grammar and style
- Ensure consistent tone
- Provide constructive feedback

Always aim to elevate the quality of content.
Reply 'TERMINATE' when the task is complete.""",
        llm_config=llm_config
    )


def create_critic_agent(llm_config: dict) -> AssistantAgent:
    """Create a critic agent for debate and feedback."""
    return create_assistant_agent(
        name="Critic",
        system_message="""You are a constructive critic.

Your responsibilities:
- Identify potential issues or gaps
- Provide balanced feedback
- Suggest improvements
- Challenge assumptions when needed

Be constructive, not destructive.
Reply 'TERMINATE' when the task is complete.""",
        llm_config=llm_config
    )


# ============================================================================
# TWO-AGENT CONVERSATION
# ============================================================================

def run_two_agent_chat(
    message: str,
    llm_config: dict
) -> str:
    """
    Run a simple two-agent conversation.
    
    Args:
        message: Initial message
        llm_config: LLM configuration
        
    Returns:
        Conversation result
    """
    if not AUTOGEN_AVAILABLE:
        return "AutoGen not installed. Please install with: pip install pyautogen"
    
    # Create assistant
    assistant = create_assistant_agent(
        name="Assistant",
        system_message="You are a helpful AI assistant. Reply TERMINATE when the task is done.",
        llm_config=llm_config
    )
    
    # Create user proxy
    user_proxy = create_user_proxy(
        name="User",
        human_input_mode="NEVER"
    )
    
    # Start conversation
    user_proxy.initiate_chat(
        assistant,
        message=message
    )
    
    return "Conversation completed"


# ============================================================================
# GROUP CHAT (MULTI-AGENT)
# ============================================================================

def create_research_group_chat(
    llm_config: dict
) -> tuple:
    """
    Create a group chat with multiple specialized agents.
    
    Returns:
        Tuple of (group_chat, user_proxy)
    """
    if not AUTOGEN_AVAILABLE:
        raise ImportError("AutoGen not installed")
    
    # Create specialized agents
    researcher = create_researcher_agent(llm_config)
    writer = create_writer_agent(llm_config)
    editor = create_editor_agent(llm_config)
    critic = create_critic_agent(llm_config)
    
    # Create user proxy
    user_proxy = create_user_proxy(
        name="Admin",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=0
    )
    
    # Create group chat
    group_chat = GroupChat(
        agents=[user_proxy, researcher, writer, editor, critic],
        messages=[],
        max_round=15,
        speaker_selection_method="round_robin"  # or "auto" or "random"
    )
    
    # Create group chat manager
    manager = GroupChatManager(
        groupchat=group_chat,
        llm_config={"config_list": [llm_config]}
    )
    
    return group_chat, user_proxy, manager


def run_group_chat(
    message: str,
    llm_config: dict
) -> str:
    """
    Run a group chat with multiple agents.
    
    Args:
        message: Initial message/task
        llm_config: LLM configuration
        
    Returns:
        Result summary
    """
    if not AUTOGEN_AVAILABLE:
        return "AutoGen not installed. Please install with: pip install pyautogen"
    
    print(f"\n{'='*60}")
    print("Starting Group Chat")
    print(f"{'='*60}\n")
    
    # Create group chat
    _, user_proxy, manager = create_research_group_chat(llm_config)
    
    # Start conversation
    user_proxy.initiate_chat(
        manager,
        message=message
    )
    
    return "Group chat completed"


# ============================================================================
# CODE EXECUTION EXAMPLE
# ============================================================================

def run_code_execution_example(llm_config: dict) -> str:
    """
    Example of agents that can execute code.
    
    This demonstrates the code execution capability of AutoGen.
    """
    if not AUTOGEN_AVAILABLE:
        return "AutoGen not installed. Please install with: pip install pyautogen"
    
    # Create assistant that writes code
    coder = create_assistant_agent(
        name="Coder",
        system_message="""You are a Python developer.
        
When asked to solve a problem:
1. Write Python code to solve it
2. The code will be executed automatically
3. Review the results and fix any errors

Always wrap code in ```python blocks.
Reply TERMINATE when the task is complete.""",
        llm_config=llm_config
    )
    
    # Create user proxy that can execute code
    user_proxy = UserProxyAgent(
        name="User",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=10,
        code_execution_config={
            "work_dir": "coding",
            "use_docker": False,
        },
    )
    
    # Start conversation
    user_proxy.initiate_chat(
        coder,
        message="Calculate the first 20 Fibonacci numbers and plot them."
    )
    
    return "Code execution completed"


# ============================================================================
# HIERARCHICAL CHAT EXAMPLE
# ============================================================================

def run_hierarchical_chat(
    task: str,
    llm_config: dict
) -> str:
    """
    Run a hierarchical chat where a manager coordinates agents.
    """
    if not AUTOGEN_AVAILABLE:
        return "AutoGen not installed. Please install with: pip install pyautogen"
    
    # Create manager agent
    manager = create_assistant_agent(
        name="Manager",
        system_message="""You are a project manager.
        
Your responsibilities:
- Break down tasks into subtasks
- Delegate to appropriate team members
- Review and integrate results
- Ensure quality and completeness

Available team members:
- Researcher: For gathering information
- Writer: For creating content
- Editor: For reviewing content

Coordinate the team to complete tasks efficiently.
Reply TERMINATE when the task is complete.""",
        llm_config=llm_config
    )
    
    # Create worker agents
    researcher = create_researcher_agent(llm_config)
    writer = create_writer_agent(llm_config)
    editor = create_editor_agent(llm_config)
    
    # Create user proxy
    user_proxy = create_user_proxy(
        name="Admin",
        human_input_mode="NEVER"
    )
    
    # Create group chat with manager
    group_chat = GroupChat(
        agents=[user_proxy, manager, researcher, writer, editor],
        messages=[],
        max_round=20,
        speaker_selection_method="auto"
    )
    
    chat_manager = GroupChatManager(
        groupchat=group_chat,
        llm_config={"config_list": [llm_config]}
    )
    
    # Start conversation
    user_proxy.initiate_chat(
        chat_manager,
        message=task
    )
    
    return "Hierarchical chat completed"


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("WARNING: OPENAI_API_KEY not set.")
        print("Set it with: export OPENAI_API_KEY='your-key-here'")
        print("\nRunning in demo mode...\n")
    
    if AUTOGEN_AVAILABLE:
        # Get configuration
        llm_config = get_llm_config()
        
        # Example 1: Two-agent chat
        print("\n" + "="*60)
        print("EXAMPLE 1: Two-Agent Chat")
        print("="*60)
        run_two_agent_chat(
            "Explain what agentic AI is in 3 sentences.",
            llm_config
        )
        
        # Example 2: Group chat
        print("\n" + "="*60)
        print("EXAMPLE 2: Group Chat (Multi-Agent)")
        print("="*60)
        run_group_chat(
            "Research and write a brief summary about LangGraph.",
            llm_config
        )
    else:
        # Show structure when AutoGen is not installed
        print("\n" + "="*60)
        print("MULTI-AGENT STRUCTURE (AutoGen)")
        print("="*60)
        print("""
    +-------------------+
    |    UserProxy      |  <-- Represents human user
    +-------------------+
            |
            v
    +-------------------+
    | GroupChatManager  |  <-- Coordinates conversation
    +-------------------+
            |
    +-------+-------+-------+-------+
    |       |       |       |       |
    v       v       v       v       v
+--------+ +--------+ +--------+ +--------+
|Research| | Writer | | Editor | | Critic |
+--------+ +--------+ +--------+ +--------+
    """)
        
        print("\nCOMMUNICATION PATTERNS:")
        print("""
    Two-Agent Chat:
    User <--> Assistant
    
    Group Chat:
    Multiple agents communicate through a shared chat
    
    Hierarchical:
    Manager coordinates workers
        """)
        
        print("\nINSTALLATION:")
        print("    pip install pyautogen")
        print("\nREQUIRED ENVIRONMENT VARIABLES:")
        print("    OPENAI_API_KEY - For LLM calls")
        
        print("\nKEY FEATURES:")
        print("    - Automatic code execution")
        print("    - Human-in-the-loop support")
        print("    - Multiple conversation patterns")
        print("    - Tool integration")