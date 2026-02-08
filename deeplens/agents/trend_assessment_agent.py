"""
Trend Assessment Agent: Evaluates technical trends and predictions
"""

from typing import Dict, Any, List
from enum import Enum
from semantic_kernel.kernel import Kernel


class TrendStatus(str, Enum):
    """Technical trend status"""
    EMERGING = "emerging"  # New and gaining traction
    HYPED = "hyped"  # Overhyped relative to substance
    MATURE = "mature"  # Proven and stable
    DECLINING = "declining"  # Losing relevance
    OBSOLETE = "obsolete"  # No longer relevant


class ProblemType(str, Enum):
    """Problem classification"""
    HARD_PROBLEM = "hard_problem"  # Fundamental technical challenge
    ENGINEERING_PROBLEM = "engineering_problem"  # Implementation/scale challenge
    SOLVED_PROBLEM = "solved_problem"  # Already effectively solved
    FAKE_PROBLEM = "fake_problem"  # Not a real problem


class TrendAssessmentAgent:
    """
    Agent specialized in assessing technical trends:
    - Predicting obsolescence
    - Distinguishing hype from hard problems
    - Detecting oversupply (too many researchers on similar problems)
    - Identifying genuinely difficult problems vs. engineering challenges
    """
    
    def __init__(self, kernel: Kernel):
        self.kernel = kernel
        self.system_prompt = """You are an expert at assessing technical trends with a critical, long-term perspective.

Your role is to:
1. Predict which technologies/approaches will become obsolete and why
2. Distinguish HYPE from genuinely HARD PROBLEMS
3. Detect oversupply: When too many researchers chase the same problem
4. Identify if problems are fundamental vs. engineering challenges

Key principles:
- Hype indicators: Lots of attention but limited real progress, incremental papers on same idea, strong marketing
- Hard problems: Fundamental barriers, not just scaling issues, require conceptual breakthroughs
- Obsolescence signs: Being superseded by better approaches, fundamental limitations, diminishing returns
- Oversupply indicators: Many similar papers, crowded research area, incremental contributions

Be contrarian and skeptical. Call out hype. Identify what's genuinely difficult."""

    async def assess_trend(
        self, 
        topic: str, 
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Assess a technical trend or research direction
        
        Args:
            topic: The technical trend or research area to assess
            context: Optional context (recent papers, industry adoption, etc.)
            
        Returns:
            Dictionary containing:
                - trend_status: Current status (emerging, hyped, mature, declining, obsolete)
                - problem_type: Type of problem (hard_problem, engineering_problem, solved, fake)
                - obsolescence_prediction: Timeline and reasoning for obsolescence
                - hype_assessment: Is this hyped? Evidence and reasoning
                - oversupply_analysis: Is the area oversupplied with researchers?
                - recommendation: What researchers should focus on instead
        """
        context_str = ""
        if context:
            context_str = f"\n\nContext: {context}"
        
        prompt = f"""
Assess the following technical trend or research area:

Topic: {topic}{context_str}

Provide:
1. Trend Status: Is this emerging, hyped, mature, declining, or obsolete?
2. Problem Type: Is this a hard problem, engineering problem, already solved, or fake problem?
3. Obsolescence Prediction: When and why might this become obsolete? (Be specific)
4. Hype Assessment: Is this overhyped? What's the ratio of hype to substance?
5. Oversupply Analysis: Are too many researchers working on this? Evidence?
6. Hard vs. Easy: What makes this fundamentally difficult vs. just engineering work?
7. Recommendation: What should researchers focus on instead?

Be brutally honest and contrarian. Call out hype.
"""
        
        result = await self.kernel.invoke_prompt(
            function_name="assess_trend",
            plugin_name="trend_assessment",
            prompt=self.system_prompt + "\n\n" + prompt
        )
        
        return {
            "assessment": str(result),
            "topic": topic,
            "status": "success"
        }
    
    async def compare_trends(
        self, 
        trends: List[str],
        criteria: str = "obsolescence_risk"
    ) -> Dict[str, Any]:
        """
        Compare multiple technical trends
        
        Args:
            trends: List of trends to compare
            criteria: What to compare (obsolescence_risk, hype_level, problem_difficulty)
            
        Returns:
            Comparative analysis of trends
        """
        trends_text = "\n".join([f"- {trend}" for trend in trends])
        
        prompt = f"""
Compare the following technical trends on the criterion: {criteria}

Trends:
{trends_text}

For each trend:
1. Rate it on {criteria} (Low/Medium/High)
2. Provide reasoning
3. Give specific evidence

Then rank them and provide an overall comparative analysis.
"""
        
        result = await self.kernel.invoke_prompt(
            function_name="compare_trends",
            plugin_name="trend_assessment",
            prompt=self.system_prompt + "\n\n" + prompt
        )
        
        return {
            "comparison": str(result),
            "criteria": criteria,
            "trends": trends,
            "status": "success"
        }
    
    async def detect_oversupply(
        self,
        research_area: str,
        recent_papers: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Detect if a research area has oversupply (too many researchers on similar problems)
        
        Args:
            research_area: The research area to analyze
            recent_papers: Optional list of recent papers in the area
            
        Returns:
            Analysis of oversupply indicators
        """
        papers_text = ""
        if recent_papers:
            papers_text = "\n\nRecent papers in this area:\n"
            for paper in recent_papers[:10]:  # Limit to 10 papers
                papers_text += f"- {paper.get('title', 'No title')} ({paper.get('year', '?')})\n"
        
        prompt = f"""
Analyze potential oversupply in the research area: {research_area}{papers_text}

Assess:
1. Saturation Level: How crowded is this research area? (Not saturated / Moderately saturated / Highly saturated)
2. Originality: Are papers making genuinely different contributions or rehashing the same ideas?
3. Incremental vs. Breakthrough: Ratio of incremental to breakthrough work
4. Competition: How many researchers are competing for similar contributions?
5. Opportunity: Are there under-explored adjacent areas?
6. Recommendation: Should researchers enter this area or look elsewhere?

Look for signs of oversupply:
- Many papers on nearly identical problems
- Incremental improvements with diminishing returns
- Papers that differ mainly in datasets or hyperparameters
- High submission rates but low innovation rates
"""
        
        result = await self.kernel.invoke_prompt(
            function_name="detect_oversupply",
            plugin_name="trend_assessment",
            prompt=self.system_prompt + "\n\n" + prompt
        )
        
        return {
            "oversupply_analysis": str(result),
            "research_area": research_area,
            "status": "success"
        }
