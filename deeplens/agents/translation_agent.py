"""
Translation Agent: Translates research buzzwords and papers into plain language
"""

from typing import Dict, Any
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.kernel import Kernel


class TranslationAgent:
    """
    Agent specialized in translating technical research language into plain English.
    Breaks down complex buzzwords, jargon, and academic papers into accessible explanations.
    """
    
    def __init__(self, kernel: Kernel):
        self.kernel = kernel
        self.system_prompt = """You are an expert at translating complex research papers and technical buzzwords into plain, accessible language.

Your role is to:
1. Identify and explain technical jargon and buzzwords
2. Break down complex concepts into simple, everyday language
3. Use analogies and examples to make ideas clear
4. Maintain accuracy while simplifying
5. Highlight what's genuinely novel vs. rebranded existing concepts

When analyzing text:
- Define all technical terms in simple language
- Explain the core idea in one sentence
- Provide concrete examples or analogies
- Point out any marketing hype vs. technical substance"""

    async def translate(self, content: str) -> Dict[str, Any]:
        """
        Translate research content into plain language
        
        Args:
            content: Research paper text, abstract, or buzzword to translate
            
        Returns:
            Dictionary containing:
                - simplified: Plain language explanation
                - key_terms: Dictionary of technical terms and their definitions
                - core_idea: One-sentence summary
                - analogies: Helpful comparisons
        """
        prompt = f"""
Analyze and translate the following research content into plain language:

{content}

Provide:
1. A simplified explanation (2-3 paragraphs)
2. Key technical terms with plain definitions
3. The core idea in one sentence
4. Helpful analogies or examples
"""
        
        # Use kernel to execute the translation
        result = await self.kernel.invoke_prompt(
            function_name="translate_research",
            plugin_name="translation",
            prompt=self.system_prompt + "\n\n" + prompt
        )
        
        return {
            "simplified": str(result),
            "status": "success"
        }
    
    async def explain_buzzword(self, buzzword: str) -> Dict[str, Any]:
        """
        Explain a specific research buzzword or term
        
        Args:
            buzzword: Technical term or buzzword to explain
            
        Returns:
            Dictionary with plain language explanation and context
        """
        prompt = f"""
Explain the research buzzword "{buzzword}" in plain language.

Provide:
1. What it actually means (stripped of hype)
2. The underlying technical concept
3. Why it became popular
4. Whether it's genuinely new or rebranded
5. A simple analogy
"""
        
        result = await self.kernel.invoke_prompt(
            function_name="explain_buzzword",
            plugin_name="translation",
            prompt=self.system_prompt + "\n\n" + prompt
        )
        
        return {
            "explanation": str(result),
            "buzzword": buzzword,
            "status": "success"
        }
