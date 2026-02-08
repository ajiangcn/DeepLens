"""
Researcher Evaluation Agent: Evaluates researcher patterns and strategies
"""

from typing import Dict, Any, List
from enum import Enum

from ..base_agent import BaseAgent
from ..registry import register_agent


class ResearcherPattern(str, Enum):
    """Researcher strategy classification"""
    TREND_FOLLOWER = "trend_follower"  # Follows hot topics and trends
    DEEP_SPECIALIST = "deep_specialist"  # Goes deep on specific problems
    ABSTRACTION_UPLEVELER = "abstraction_upleveler"  # Works on higher-level problem abstractions


@register_agent("researcher")
class ResearcherEvaluationAgent(BaseAgent):
    """
    Agent specialized in evaluating researcher history to determine their strategy:
    - Trend Follower: Jumps between hot topics
    - Deep Specialist: Sustained deep work on core problems
    - Abstraction Upleveler: Progressively tackles more fundamental problems
    """
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for researcher evaluation agent"""
        return """You are an expert at analyzing researcher career patterns and strategies.

Your role is to identify whether a researcher:
1. TREND FOLLOWER: Moves between hot topics, following what's popular
   - Signs: Topic shifts align with hype cycles, many different areas, surface-level contributions
   
2. DEEP SPECIALIST: Goes deep on specific problems with sustained focus
   - Signs: Sustained work on related problems, builds on own foundations, systematic progress
   
3. ABSTRACTION UPLEVELER: Progressively works on more fundamental problems
   - Signs: Work shows progression from specific to general, tackles underlying causes, framework building

When analyzing researcher history:
- Look at topic progression over time
- Assess depth vs. breadth of contributions
- Identify if work builds systematically or jumps around
- Consider if they're solving symptoms vs. root causes
- Evaluate if they're creating new problem framings"""

    async def evaluate_researcher(
        self, 
        publications: List[Dict[str, Any]], 
        researcher_name: str = None
    ) -> Dict[str, Any]:
        """
        Evaluate a researcher's pattern based on their publication history
        
        Args:
            publications: List of publications with titles, abstracts, years
            researcher_name: Optional researcher name for context
            
        Returns:
            Dictionary containing:
                - pattern: Primary research pattern (trend_follower, deep_specialist, abstraction_upleveler)
                - confidence: Confidence in the classification (0-1)
                - reasoning: Detailed explanation of the classification
                - key_indicators: Specific evidence supporting the classification
                - trajectory: Description of career trajectory
                - topic_evolution: How topics have evolved over time
        """
        # Format publications for analysis
        pubs_text = "\n\n".join([
            f"Year {pub.get('year', 'Unknown')}: {pub.get('title', 'No title')}\n"
            f"Abstract: {pub.get('abstract', 'No abstract')[:300]}..."
            for pub in publications
        ])
        
        name_context = f" for researcher {researcher_name}" if researcher_name else ""
        
        prompt = f"""
Analyze the following publication history{name_context}:

{pubs_text}

Classify the researcher as:
1. TREND FOLLOWER: Follows hot topics and trends
2. DEEP SPECIALIST: Goes deep on specific problems
3. ABSTRACTION UPLEVELER: Works on progressively more fundamental problems

Provide:
1. Primary Pattern: Which pattern best describes them?
2. Confidence: How confident are you? (Low/Medium/High)
3. Reasoning: Detailed explanation with specific examples
4. Key Indicators: Concrete evidence from their work
5. Trajectory: How has their work evolved?
6. Topic Evolution: Describe the progression (or lack thereof) in topics
"""
        
        result = await self.invoke_prompt(
            prompt=prompt
        )
        
        return {
            "evaluation": result,
            "status": "success"
        }
    
    async def compare_researchers(
        self, 
        researchers_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Compare multiple researchers' patterns
        
        Args:
            researchers_data: List of dicts with researcher info and publications
            
        Returns:
            Comparative analysis of researcher patterns
        """
        researchers_text = ""
        for i, researcher in enumerate(researchers_data, 1):
            name = researcher.get('name', f'Researcher {i}')
            pubs = researcher.get('publications', [])
            researchers_text += f"\n\n=== {name} ===\n"
            for pub in pubs[:5]:  # Limit to 5 pubs per researcher for comparison
                researchers_text += f"- {pub.get('year', '?')}: {pub.get('title', 'No title')}\n"
        
        prompt = f"""
Compare the following researchers and their work patterns:

{researchers_text}

For each researcher:
1. Classify their pattern (Trend Follower, Deep Specialist, or Abstraction Upleveler)
2. Provide key distinguishing characteristics
3. Compare and contrast their approaches

Then provide an overall comparative analysis.
"""
        
        result = await self.invoke_prompt(
            prompt=prompt
        )
        
        return {
            "comparison": result,
            "status": "success"
        }
