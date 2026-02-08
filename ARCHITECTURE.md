# DeepLens Architecture

## Overview

DeepLens is built on Microsoft's Semantic Kernel framework, which provides a flexible multi-agent architecture for AI applications.

## System Components

### 1. Orchestrator Layer

**DeepLensOrchestrator** (`deeplens/orchestrator.py`)
- Central coordination point for all agents
- Manages Semantic Kernel initialization
- Provides high-level API for common tasks
- Handles agent lifecycle and communication

### 2. Agent Layer

Four specialized agents, each with a distinct purpose:

#### TranslationAgent (`deeplens/agents/translation_agent.py`)
**Purpose**: Simplify research jargon and buzzwords

**Key Methods**:
- `translate(content)` - Translate research papers/abstracts
- `explain_buzzword(buzzword)` - Explain specific terms

**System Prompt Focus**:
- Identify and explain technical jargon
- Break down complex concepts
- Use analogies and examples
- Distinguish genuinely novel concepts from rebranding

#### AnalysisAgent (`deeplens/agents/analysis_agent.py`)
**Purpose**: Identify fundamental problems and research maturity

**Key Methods**:
- `analyze(content, context)` - Comprehensive research analysis
- `identify_problem_hierarchy(content)` - Problem abstraction levels

**System Prompt Focus**:
- Identify FUNDAMENTAL problems (beyond surface claims)
- Classify research stage (Exploration/Scaling/Convergence)
- Assess genuine industry demand vs. speculation
- Distinguish technical vs. engineering challenges

**Research Stages**:
- **Exploration**: New problem space, early investigation
- **Scaling**: Proven concept, focusing on efficiency and scale
- **Convergence**: Mature field, incremental improvements

#### ResearcherEvaluationAgent (`deeplens/agents/researcher_evaluation_agent.py`)
**Purpose**: Evaluate researcher strategies and patterns

**Key Methods**:
- `evaluate_researcher(publications, researcher_name)` - Pattern analysis
- `compare_researchers(researchers_data)` - Comparative analysis

**System Prompt Focus**:
- Identify researcher patterns:
  - **Trend Follower**: Jumps between hot topics
  - **Deep Specialist**: Sustained focus on core problems
  - **Abstraction Upleveler**: Progressive work on fundamental problems
- Analyze topic progression over time
- Assess depth vs. breadth of contributions

#### TrendAssessmentAgent (`deeplens/agents/trend_assessment_agent.py`)
**Purpose**: Assess trends, hype, and future predictions

**Key Methods**:
- `assess_trend(topic, context)` - Comprehensive trend analysis
- `compare_trends(trends, criteria)` - Multi-trend comparison
- `detect_oversupply(research_area, recent_papers)` - Oversupply detection

**System Prompt Focus**:
- Predict obsolescence and timelines
- Distinguish hype from genuinely hard problems
- Detect oversupply (too many researchers on similar problems)
- Identify fundamental vs. engineering challenges
- Be contrarian and skeptical

**Trend Status Classifications**:
- **Emerging**: New and gaining traction
- **Hyped**: Overhyped relative to substance
- **Mature**: Proven and stable
- **Declining**: Losing relevance
- **Obsolete**: No longer relevant

**Problem Type Classifications**:
- **Hard Problem**: Fundamental technical challenge
- **Engineering Problem**: Implementation/scale challenge
- **Solved Problem**: Already effectively solved
- **Fake Problem**: Not a real problem

## Data Flow

```
User Request
     ↓
DeepLensOrchestrator
     ↓
Semantic Kernel
     ↓
Agent (with System Prompt + User Prompt)
     ↓
LLM (GPT-4)
     ↓
Agent (processes response)
     ↓
DeepLensOrchestrator
     ↓
User Response
```

## Agent Design Patterns

### System Prompts
Each agent has a carefully crafted system prompt that:
1. Defines the agent's role and expertise
2. Specifies key principles and focus areas
3. Provides guidance on analysis approach
4. Sets the tone (skeptical, contrarian for TrendAssessmentAgent)

### Prompt Construction
For each user request:
1. System prompt (defines agent personality and expertise)
2. Task-specific instructions (what to analyze and return)
3. User content (the actual research to analyze)
4. Format specifications (structured output requirements)

### Response Processing
Agents return structured dictionaries containing:
- Primary analysis results
- Metadata (status, input parameters)
- Structured components (simplified text, classifications, etc.)

## Extensibility

### Adding New Agents
1. Create agent class in `deeplens/agents/`
2. Define `__init__(kernel)` method
3. Add system prompt defining agent expertise
4. Implement analysis methods using `kernel.invoke_prompt()`
5. Update `DeepLensOrchestrator` to initialize and expose the agent

### Adding New Analysis Types
1. Add method to appropriate agent
2. Define task-specific prompt template
3. Return structured dictionary with results
4. Update orchestrator with convenience method (optional)

## Configuration

### API Providers
- **OpenAI** (default): Standard OpenAI API
- **Azure OpenAI** (coming soon): Azure-hosted OpenAI

### Model Selection
Default: `gpt-4` (recommended for quality)
Alternatives: `gpt-3.5-turbo` (faster, cheaper)

## Error Handling

Agents use try-catch patterns to handle:
- API errors (rate limits, authentication)
- Malformed inputs
- Unexpected LLM responses

Status codes in responses:
- `"success"` - Operation completed
- `"error"` - Operation failed (with error details)

## Performance Considerations

### Parallel Execution
The orchestrator supports parallel agent calls for independent tasks:
```python
results = await orchestrator.comprehensive_analysis(
    research_content=paper,
    trend_topics=["LLMs", "Vision Transformers"],
    researcher_publications=pubs
)
```

### Rate Limiting
Handled by Semantic Kernel and OpenAI client libraries

### Future Enhancements
Potential improvements for future versions:
- **Caching**: Cache common queries at orchestrator or kernel level
- **Batch Processing**: Process multiple requests in parallel
- **Custom Models**: Support for other LLM providers

## Testing Strategy

### Unit Tests
Test individual agent methods with mock Kernel

### Integration Tests
Test orchestrator with real or mocked LLM responses

### End-to-End Tests
Test full workflows with sample data

## Dependencies

Core framework:
- `semantic-kernel` - Microsoft's agent framework
- `openai` - OpenAI API client

Supporting libraries:
- `pydantic` - Data validation
- `python-dotenv` - Configuration management
- `aiohttp` - Async HTTP client
