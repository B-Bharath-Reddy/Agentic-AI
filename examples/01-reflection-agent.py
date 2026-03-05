"""
Reflection Agent Example
========================
A complete implementation of the Reflection design pattern.

This agent:
1. Generates an initial output (code, text, etc.)
2. Reviews its own output for errors/improvements
3. Iteratively refines until satisfied or max iterations reached
"""

import os
from typing import Optional, List, Dict
from dataclasses import dataclass
from enum import Enum

# Try to import aisuite, fallback to openai
try:
    import aisuite as ai
    CLIENT = ai.Client()
    USE_AISUITE = True
except ImportError:
    import openai
    CLIENT = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    USE_AISUITE = False


class TaskType(Enum):
    CODE_GENERATION = "code_generation"
    EMAIL_WRITING = "email_writing"
    ESSAY_WRITING = "essay_writing"
    GENERAL = "general"


@dataclass
class ReflectionResult:
    """Result of a reflection iteration"""
    iteration: int
    draft: str
    critique: str
    improved: bool
    final_output: Optional[str] = None


# ============================================================================
# REFLECTION PROMPTS
# ============================================================================

REFLECTION_PROMPTS = {
    TaskType.CODE_GENERATION: """
Review the following code for:
1. Correctness - Does it solve the problem?
2. Edge cases - Are edge cases handled?
3. Style - Is it readable and well-structured?
4. Efficiency - Can it be optimized?

Code to review:
```
{draft}
```

Provide specific, actionable feedback. Then provide an improved version.
""",
    
    TaskType.EMAIL_WRITING: """
Review the following email for:
1. Tone - Is it professional and appropriate?
2. Clarity - Is the message clear?
3. Completeness - Are all necessary details included?
4. Rudeness check - Could any phrase be perceived negatively?

Email to review:
```
{draft}
```

Provide specific feedback. Then write an improved version.
""",
    
    TaskType.ESSAY_WRITING: """
Review the following essay for:
1. Structure - Is there a clear introduction, body, conclusion?
2. Arguments - Are arguments well-supported?
3. Clarity - Is the writing clear and concise?
4. Completeness - Are all required points addressed?

Essay to review:
```
{draft}
```

Provide specific feedback. Then write an improved version.
""",
    
    TaskType.GENERAL: """
Review the following output for quality, accuracy, and completeness.
Identify any issues and suggest improvements.

Output to review:
```
{draft}
```

Provide specific feedback. Then provide an improved version.
"""
}


# ============================================================================
# REFLECTION AGENT
# ============================================================================

class ReflectionAgent:
    """
    An agent that uses self-reflection to improve outputs.
    
    Usage:
        agent = ReflectionAgent()
        result = agent.run("Write a function to sort a list", TaskType.CODE_GENERATION)
        print(result.final_output)
    """
    
    def __init__(
        self,
        model: str = "openai:gpt-4o",
        max_iterations: int = 3,
        verbose: bool = True
    ):
        self.model = model
        self.max_iterations = max_iterations
        self.verbose = verbose
        self.history: List[ReflectionResult] = []
    
    def _call_llm(self, messages: List[Dict]) -> str:
        """Call the LLM with the given messages"""
        if USE_AISUITE:
            response = CLIENT.chat.completions.create(
                model=self.model,
                messages=messages
            )
        else:
            # Strip 'openai:' prefix for direct OpenAI usage
            model = self.model.replace("openai:", "")
            response = CLIENT.chat.completions.create(
                model=model,
                messages=messages
            )
        return response.choices[0].message.content
    
    def generate_initial(self, task: str, task_type: TaskType) -> str:
        """Generate initial draft"""
        system_prompt = f"You are an expert at {task_type.value.replace('_', ' ')}."
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": task}
        ]
        
        return self._call_llm(messages)
    
    def reflect(self, draft: str, task_type: TaskType) -> tuple[str, str]:
        """
        Reflect on the draft and provide improved version.
        Returns (critique, improved_version)
        """
        prompt = REFLECTION_PROMPTS[task_type].format(draft=draft)
        
        messages = [
            {"role": "system", "content": "You are a thoughtful reviewer who provides constructive feedback."},
            {"role": "user", "content": prompt}
        ]
        
        response = self._call_llm(messages)
        
        # Parse critique and improved version
        # The response should contain both feedback and improved version
        return response, response
    
    def run(
        self,
        task: str,
        task_type: TaskType = TaskType.GENERAL,
        stop_when_satisfied: bool = True
    ) -> ReflectionResult:
        """
        Run the reflection loop.
        
        Args:
            task: The task to complete
            task_type: Type of task (affects reflection prompts)
            stop_when_satisfied: Whether to stop when LLM indicates satisfaction
        
        Returns:
            ReflectionResult with final output
        """
        self.history = []
        
        # Step 1: Generate initial draft
        if self.verbose:
            print("=" * 60)
            print("[INFO] Generating initial draft...")
            print("=" * 60)
        
        current_draft = self.generate_initial(task, task_type)
        
        if self.verbose:
            print(f"\n{current_draft}\n")
        
        # Step 2: Reflection loop
        for i in range(self.max_iterations):
            if self.verbose:
                print("=" * 60)
                print(f"[REFLECTION] Iteration {i + 1}/{self.max_iterations}")
                print("=" * 60)
            
            critique, improved = self.reflect(current_draft, task_type)
            
            # Check if improvement was made
            improved_flag = improved != current_draft
            
            result = ReflectionResult(
                iteration=i + 1,
                draft=current_draft,
                critique=critique,
                improved=improved_flag
            )
            
            self.history.append(result)
            
            if self.verbose:
                print(f"\n[CRITIQUE]:\n{critique[:500]}...\n")
            
            # Check for satisfaction markers
            if stop_when_satisfied:
                satisfaction_markers = [
                    "no further improvements",
                    "looks good",
                    "satisfactory",
                    "no changes needed",
                    "final version"
                ]
                if any(marker in critique.lower() for marker in satisfaction_markers):
                    if self.verbose:
                        print("[SUCCESS] Agent is satisfied with the output!")
                    break
            
            current_draft = improved
        
        # Return final result
        final_result = ReflectionResult(
            iteration=len(self.history),
            draft=current_draft,
            critique="",
            improved=True,
            final_output=current_draft
        )
        
        if self.verbose:
            print("=" * 60)
            print("[FINAL OUTPUT]")
            print("=" * 60)
            print(current_draft)
        
        return final_result


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

def example_code_generation():
    """Example: Code generation with reflection"""
    print("\n" + "=" * 60)
    print("EXAMPLE: Code Generation with Reflection")
    print("=" * 60 + "\n")
    
    agent = ReflectionAgent(max_iterations=2, verbose=True)
    
    task = """
    Write a Python function that calculates the factorial of a number.
    Include error handling for edge cases.
    """
    
    result = agent.run(task, TaskType.CODE_GENERATION)
    return result


def example_email_writing():
    """Example: Email writing with reflection"""
    print("\n" + "=" * 60)
    print("EXAMPLE: Email Writing with Reflection")
    print("=" * 60 + "\n")
    
    agent = ReflectionAgent(max_iterations=2, verbose=True)
    
    task = """
    Write a professional email to a client explaining that their project 
    deadline needs to be extended by 2 weeks due to unexpected technical 
    challenges. Be apologetic but confident.
    """
    
    result = agent.run(task, TaskType.EMAIL_WRITING)
    return result


def example_with_external_feedback():
    """
    Example: Reflection with external feedback (code execution)
    
    This shows how to use external tools (like code execution) 
    to provide feedback for reflection.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE: Reflection with External Feedback")
    print("=" * 60 + "\n")
    
    def execute_code(code: str) -> tuple[bool, str]:
        """Execute code and return (success, output/error)"""
        try:
            # Create a namespace for execution
            namespace = {}
            exec(code, namespace)
            return True, "Code executed successfully!"
        except Exception as e:
            return False, f"Error: {type(e).__name__}: {str(e)}"
    
    agent = ReflectionAgent(max_iterations=3, verbose=True)
    
    task = "Write a Python function that returns the sum of squares from 1 to n"
    
    # Generate initial draft
    draft = agent.generate_initial(task, TaskType.CODE_GENERATION)
    print(f"Initial draft:\n{draft}\n")
    
    # Try to execute
    success, output = execute_code(draft)
    
    if not success:
        print(f"[ERROR] Execution failed: {output}")
        print("\n[INFO] Reflecting on error...")
        
        # Feed error back for reflection
        error_feedback = f"""
The code you wrote failed to execute:
```
{draft}
```

Error:
{output}

Please fix the code and provide a working version.
"""
        # Use the agent to fix
        messages = [
            {"role": "system", "content": "You are a Python expert. Fix the code."},
            {"role": "user", "content": error_feedback}
        ]
        fixed = agent._call_llm(messages)
        print(f"\n[FIXED]:\n{fixed}")
        
        # Verify fix
        success, output = execute_code(fixed)
        if success:
            print(f"\n[SUCCESS] {output}")
        else:
            print(f"\n[ERROR] Still has issues: {output}")
    
    return draft


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("    REFLECTION AGENT - Example Implementation")
    print("=" * 60)
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("\n[WARNING] OPENAI_API_KEY not set.")
        print("   Set it with: export OPENAI_API_KEY='your-key-here'")
        print("\n   Running in demo mode (showing structure only)...\n")
    else:
        # Run examples
        # Uncomment to run:
        # example_code_generation()
        # example_email_writing()
        # example_with_external_feedback()
        pass
    
    # Show the structure
    print("\n[REFLECTION AGENT STRUCTURE]:")
    print("""
    +-------------------------------------------------------------+
    |                    REFLECTION WORKFLOW                       |
    |                                                              |
    |   +----------+    +----------+    +----------+              |
    |   |  Write   |--->| Review/  |--->| Reflect  |              |
    |   |  Draft   |    | Critique |    | & Revise |              |
    |   +----------+    +----------+    +----------+              |
    |                         |              |                    |
    |                         +--------------+                    |
    |                        (Iterate if needed)                  |
    +-------------------------------------------------------------+
    """)
    
    print("\n[USAGE]:")
    print("""
    from reflection_agent import ReflectionAgent, TaskType
    
    agent = ReflectionAgent(max_iterations=3)
    result = agent.run(
        "Write a function to sort a list",
        TaskType.CODE_GENERATION
    )
    print(result.final_output)
    """)
    
    print("\n[KEY FEATURES]:")
    print("   - Self-critique and improvement")
    print("   - Multiple task types supported")
    print("   - Configurable iteration limit")
    print("   - External feedback integration")
    print("   - Full history tracking")