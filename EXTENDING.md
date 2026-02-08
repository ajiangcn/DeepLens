# Extending DeepLens: Adding New Agents

This guide explains how to add new agents to the DeepLens system using the extensible architecture.

## Quick Start

Creating a new agent is simple:

```python
from deeplens.base_agent import BaseAgent
from deeplens.registry import register_agent
from semantic_kernel.kernel import Kernel
from typing import Dict, Any

@register_agent("my_agent")
class MyAgent(BaseAgent):
    """
    Description of what your agent does
    """
    
    def _get_system_prompt(self) -> str:
        """Define your agent's expertise and behavior"""
        return """You are an expert at [domain].
        
Your role is to:
1. [Capability 1]
2. [Capability 2]
3. [Capability 3]

When analyzing:
- [Guideline 1]
- [Guideline 2]
"""
    
    async def analyze(self, content: str) -> Dict[str, Any]:
        """
        Main analysis method
        
        Args:
            content: Input to analyze
            
        Returns:
            Dictionary with analysis results
        """
        prompt = f"""
Analyze the following:

{content}

Provide:
1. [What to provide]
2. [What to provide]
"""
        
        result = await self.invoke_prompt(
            prompt=prompt,
            function_name="analyze"
        )
        
        return {
            "analysis": result,
            "status": "success"
        }
```

## Step-by-Step Guide

### 1. Create Agent File

Create a new file in `deeplens/agents/` directory:

```bash
touch deeplens/agents/my_new_agent.py
```

### 2. Import Required Classes

```python
from typing import Dict, Any, Optional
from semantic_kernel.kernel import Kernel
from ..base_agent import BaseAgent
from ..registry import register_agent
```

### 3. Define Agent Class

```python
@register_agent("my_agent_name")
class MyNewAgent(BaseAgent):
    """
    Agent description here.
    Explain what problems this agent solves.
    """
```

### 4. Implement System Prompt

The system prompt defines your agent's personality and expertise:

```python
def _get_system_prompt(self) -> str:
    """Get the system prompt"""
    return """You are a [role] expert.
    
Your role is to:
1. [Primary capability]
2. [Secondary capability]
3. [Additional capability]

Key principles:
- [Principle 1]
- [Principle 2]
- Be [characteristic]
"""
```

**Tips for System Prompts:**
- Be specific about the agent's expertise
- Define clear guidelines for analysis
- Set the appropriate tone (skeptical, helpful, analytical, etc.)
- Include examples if helpful

### 5. Implement Analysis Methods

Add methods for different types of analysis:

```python
async def main_analysis(self, content: str, options: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Main analysis method
    
    Args:
        content: Content to analyze
        options: Optional parameters
        
    Returns:
        Analysis results
    """
    # Build your prompt
    prompt = f"""
Analyze: {content}

Provide:
1. [Result format]
2. [Result format]
"""
    
    # Use base class invoke_prompt method
    result = await self.invoke_prompt(
        prompt=prompt,
        function_name="main_analysis"
    )
    
    # Return structured response
    return {
        "result": result,
        "status": "success"
    }
```

### 6. Add to Orchestrator

Update `deeplens/orchestrator.py` to include your agent:

```python
from .agents.my_new_agent import MyNewAgent

class DeepLensOrchestrator:
    def __init__(self, ...):
        # ...existing code...
        self.my_agent = MyNewAgent(self.kernel)
    
    async def my_agent_method(self, content: str) -> Dict[str, Any]:
        """
        Convenience method for your agent
        """
        return await self.my_agent.main_analysis(content)
```

### 7. Add UI Support

Update `deeplens/ui.py` to add a tab for your agent:

```python
# In create_interface method, add new tab
with gr.Tab("🆕 My Agent"):
    gr.Markdown("### My Agent Description")
    with gr.Row():
        with gr.Column():
            input_box = gr.Textbox(
                label="Input",
                placeholder="Enter content...",
                lines=6
            )
            btn = gr.Button("Analyze", variant="primary")
        with gr.Column():
            output_box = gr.Markdown(label="Results")
    
    btn.click(
        fn=lambda x: asyncio.run(self.my_agent_method(x)),
        inputs=input_box,
        outputs=output_box
    )
```

### 8. Add CLI Support

Update `deeplens/interactive_cli.py`:

```python
async def my_agent_mode(self):
    """Interactive mode for my agent"""
    console.print("\n[bold cyan]🆕 My Agent Mode[/bold cyan]")
    
    content = Prompt.ask("Enter content")
    
    with Progress(...) as progress:
        progress.add_task("Analyzing...", total=None)
        orchestrator = self._get_orchestrator()
        result = await orchestrator.my_agent_method(content)
        
        console.print(Panel(
            result['result'],
            title="Results",
            border_style="green"
        ))
```

## Best Practices

### Agent Design

1. **Single Responsibility**: Each agent should focus on one type of analysis
2. **Clear Interface**: Methods should have descriptive names and clear parameters
3. **Structured Output**: Always return dictionaries with consistent keys
4. **Error Handling**: Use try-except and return informative error messages

### System Prompts

1. **Be Specific**: Clearly define the agent's role and expertise
2. **Set Expectations**: Explain what kind of output is expected
3. **Provide Context**: Give the LLM context about its purpose
4. **Include Examples**: If helpful, show example analyses

### Method Design

1. **Use Type Hints**: Always annotate types for parameters and returns
2. **Document Well**: Write clear docstrings explaining purpose and usage
3. **Validate Input**: Check inputs before processing
4. **Return Consistently**: Use same dictionary structure across methods

## Example: Citation Checker Agent

Here's a complete example of a new agent:

```python
"""
Citation Checker Agent: Validates research citations and references
"""

from typing import Dict, Any, List
from ..base_agent import BaseAgent
from ..registry import register_agent


@register_agent("citation")
class CitationCheckerAgent(BaseAgent):
    """
    Agent specialized in checking research citations and references.
    Validates citation accuracy and identifies missing citations.
    """
    
    def _get_system_prompt(self) -> str:
        return """You are an expert at analyzing research citations and references.

Your role is to:
1. Check if claims have proper citations
2. Identify missing citations for key claims
3. Assess citation quality and relevance
4. Detect potential citation issues

When analyzing:
- Look for uncited claims that need references
- Check if citations support the claims made
- Identify citation patterns (self-citation, citation cartels)
- Suggest relevant missing citations
"""
    
    async def check_citations(
        self,
        content: str,
        existing_citations: List[str] = None
    ) -> Dict[str, Any]:
        """
        Check citations in research content
        
        Args:
            content: Research text to check
            existing_citations: List of existing citations
            
        Returns:
            Citation analysis results
        """
        citations_text = ""
        if existing_citations:
            citations_text = "\n\nExisting citations:\n" + "\n".join(
                f"[{i+1}] {c}" for i, c in enumerate(existing_citations)
            )
        
        prompt = f"""
Analyze citations in this research content:

{content}{citations_text}

Provide:
1. Uncited Claims: List claims that need citations
2. Citation Quality: Are citations appropriate and relevant?
3. Missing Citations: Suggest important missing citations
4. Citation Issues: Any problems with current citations?
"""
        
        result = await self.invoke_prompt(
            prompt=prompt,
            function_name="check_citations"
        )
        
        return {
            "analysis": result,
            "status": "success"
        }
```

## Testing Your Agent

Create a simple test script:

```python
import asyncio
from deeplens import DeepLensOrchestrator

async def test_my_agent():
    orchestrator = DeepLensOrchestrator()
    
    result = await orchestrator.my_agent.analyze("test content")
    print(result)

if __name__ == "__main__":
    asyncio.run(test_my_agent())
```

## Registering Without Decorator

If you prefer not to use the decorator:

```python
from deeplens.registry import AgentRegistry

class MyAgent(BaseAgent):
    # ... agent code ...

# Register manually
AgentRegistry.register("my_agent", MyAgent)
```

## Advanced: Custom Configuration

Add agent-specific configuration:

```python
from deeplens.config import AgentConfig

# In orchestrator or UI
config = AgentConfig(
    enabled=True,
    temperature=0.5,  # Override default temperature
    max_tokens=2000
)

orchestrator.config.set_agent_config("my_agent", config)
```

## Questions?

- Check existing agents in `deeplens/agents/` for examples
- Review `BaseAgent` in `deeplens/base_agent.py` for available methods
- See `AgentRegistry` in `deeplens/registry.py` for registration details
