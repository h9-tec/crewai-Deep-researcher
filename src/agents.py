import os
from crewai import Agent
from langchain_community.chat_models import ChatOllama
from tools.browser_tool import BrowserTool

# Initialize tools
browser_tool = BrowserTool()

# Configure Ollama
ollama_base_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
ollama_model = os.getenv('OLLAMA_MODEL', 'deepseek-r1:8b')

# Create a shared Ollama configuration
ollama = ChatOllama(
    model=f"ollama/{ollama_model}",
    base_url=ollama_base_url,
    temperature=0.7,
    streaming=True,
    verbose=True
)

# Web Research Specialist
web_research_specialist = Agent(
    role='Web Research Specialist',
    goal='Search and gather accurate information from the web',
    backstory="""You are an expert at web research and information gathering. 
    Your goal is to find relevant and accurate information from reliable sources.""",
    tools=[browser_tool],
    allow_delegation=False,
    llm=ollama,
    verbose=True
)

# Content Analyzer
content_analyzer = Agent(
    role='Content Analyzer',
    goal='Analyze and synthesize research findings',
    backstory="""You are an expert at analyzing and synthesizing information.
    Your goal is to process research findings and extract key insights.""",
    tools=[browser_tool],
    allow_delegation=True,
    llm=ChatOllama(
        model=f"ollama/{ollama_model}",
        base_url=ollama_base_url,
        temperature=0.5,
        streaming=True,
        verbose=True
    ),
    verbose=True
)

# Fact Checker
fact_checker = Agent(
    role='Fact Checker',
    goal='Verify information accuracy and credibility',
    backstory="""You are an expert fact checker with a keen eye for detail.
    Your goal is to verify the accuracy of information and assess source credibility.""",
    tools=[browser_tool],
    allow_delegation=True,
    llm=ChatOllama(
        model=f"ollama/{ollama_model}",
        base_url=ollama_base_url,
        temperature=0.3,
        streaming=True,
        verbose=True
    ),
    verbose=True
)

# You can add more agents here if needed for more complex workflows