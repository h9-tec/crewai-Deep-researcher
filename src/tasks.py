from crewai import Task
from event_system import event_system

# Import the agents defined in agents.py
from agents import web_research_specialist, content_analyzer, fact_checker

def get_research_task(query: str) -> Task:
    """Create a research task for the web research specialist"""
    event_system.notify_step(
        thought="Creating research task",
        action="Task Creation",
        input_data=query,
        observation="Initializing web research task"
    )
    
    return Task(
        description=f"""Research the following topic thoroughly: {query}
        1. Search for recent and reliable information
        2. Gather key facts and insights
        3. Include relevant statistics and data
        4. Note any conflicting information
        5. Save important quotes and citations""",
        expected_output="""Detailed research findings including:
        - Key facts and insights
        - Statistics and data
        - Expert opinions
        - Source citations""",
        agent=web_research_specialist,
        context=None  # Remove context for initial task
    )

def get_analysis_task(research_results: str) -> Task:
    """Create an analysis task for the content analyzer"""
    event_system.notify_step(
        thought="Creating analysis task",
        action="Task Creation",
        input_data="Processing research results",
        observation="Initializing content analysis task"
    )
    
    return Task(
        description="""Analyze the research findings and:
        1. Identify main themes and patterns
        2. Extract key insights
        3. Organize information logically
        4. Highlight significant findings
        5. Note areas needing further research""",
        expected_output="""Comprehensive analysis including:
        - Main themes identified
        - Key insights extracted
        - Logical organization of findings
        - Areas for further research""",
        agent=content_analyzer,
        context=None  # Remove context, will be passed through crew execution
    )

def get_fact_checking_task(analysis_results: str) -> Task:
    """Create a fact checking task for the fact checker"""
    event_system.notify_step(
        thought="Creating fact checking task",
        action="Task Creation",
        input_data="Verifying analysis results",
        observation="Initializing fact checking task"
    )
    
    return Task(
        description="""Verify the analyzed information:
        1. Check accuracy of facts and statistics
        2. Verify source credibility
        3. Cross-reference key claims
        4. Identify potential biases
        5. Flag any questionable information""",
        expected_output="""Verification report including:
        - Confirmed facts and statistics
        - Source credibility assessment
        - Cross-reference results
        - Identified biases or concerns""",
        agent=fact_checker,
        context=None  # Remove context, will be passed through crew execution
    )