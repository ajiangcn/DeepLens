"""
Analysis Agent: Identifies fundamental problems, research stage, and industry demand
"""

from typing import Dict, Any, List
from enum import Enum
from semantic_kernel.kernel import Kernel
from ..base_agent import BaseAgent
from ..registry import register_agent


class ResearchStage(str, Enum):
    """Research stage classification"""
    EXPLORATION = "exploration"  # Early stage, exploring problem space
    SCALING = "scaling"  # Proven concept, focusing on scale and efficiency
    CONVERGENCE = "convergence"  # Mature field, incremental improvements


@register_agent("analysis")
class AnalysisAgent(BaseAgent):
    """
    Agent specialized in analyzing research to identify:
    - The fundamental problem being addressed
    - Current research stage (exploration/scaling/convergence)
    - Industry demand and practical applications
    """
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for analysis agent"""
        return """You are an expert research analyst who identifies the core problems, research maturity, and real-world demand.

Your role is to:
1. Identify the FUNDAMENTAL problem (not the surface-level claim)
2. Classify research stage: Exploration (new problem space), Scaling (proven, needs efficiency), or Convergence (mature, incremental)
3. Assess genuine industry demand vs. speculative interest
4. Distinguish between technical challenges and engineering challenges

When analyzing research:
- Look past buzzwords to the actual problem being solved
- Consider: Is this opening new ground, scaling proven ideas, or optimizing mature tech?
- Evaluate: Is there clear industry pull, or is this push from researchers?
- Be skeptical: Many papers claim novelty but address well-known problems"""

    async def analyze(self, content: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Analyze research content to identify problem, stage, and demand
        
        Args:
            content: Research paper, proposal, or technical description
            context: Optional additional context (related work, citations, etc.)
            
        Returns:
            Dictionary containing:
                - fundamental_problem: The core problem being addressed
                - research_stage: exploration, scaling, or convergence
                - stage_reasoning: Why this stage was assigned
                - industry_demand: Assessment of real-world demand
                - demand_evidence: Evidence for demand assessment
                - key_challenges: Main technical challenges
        """
        context_str = ""
        if context:
            context_str = f"\n\nAdditional context: {context}"
        
        prompt = f"""
Analyze the following research content:

{content}{context_str}

Provide:
1. Fundamental Problem: What is the REAL problem being solved? (Go beyond stated claims)
2. Research Stage: Is this Exploration (new territory), Scaling (proven concept, needs efficiency), or Convergence (mature field, incremental gains)?
3. Stage Reasoning: Why did you classify it this way?
4. Industry Demand: Is there genuine industry pull, or speculative/academic interest?
5. Demand Evidence: What evidence supports your demand assessment?
6. Key Challenges: What are the main technical vs. engineering challenges?
"""
        
        result = await self.invoke_prompt(
            prompt=prompt,
            function_name="analyze_research"
        )
        
        return {
            "analysis": result,
            "status": "success"
        }
    
    async def identify_problem_hierarchy(self, content: str) -> Dict[str, Any]:
        """
        Identify the hierarchy of problems from surface to fundamental
        
        Args:
            content: Research content to analyze
            
        Returns:
            Dictionary with problem hierarchy and abstraction levels
        """
        prompt = f"""
Analyze this research and identify the problem hierarchy:

{content}

List the problems from surface level to fundamental:
1. Stated Problem: What the paper claims to solve
2. Actual Problem: What it really addresses
3. Fundamental Problem: The deepest underlying issue

For each level, explain what makes it different from the others.
"""
        
        result = await self.invoke_prompt(
            prompt=prompt,
            function_name="identify_hierarchy"
        )
        
        return {
            "hierarchy": result,
            "status": "success"
        }
