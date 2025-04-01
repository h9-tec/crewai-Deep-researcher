import asyncio
import os
from crewai.tools import BaseTool
from browser_use import Agent as BrowserAgent
from langchain_community.llms import Ollama
from dotenv import load_dotenv
from event_system import event_system
from typing import Any, Dict, Optional
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re

# Load environment variables from .env file
load_dotenv()

class BrowserTool(BaseTool):
    name: str = "Browser"
    description: str = "Browse websites and extract information"

    def _run(self, task_description: str) -> str:
        """Run the browser tool with the given task description"""
        event_system.notify_step(
            thought="Starting browser task",
            action="Browser Navigation",
            input_data=task_description,
            observation="Initializing browser"
        )

        try:
            with sync_playwright() as p:
                # Launch browser
                browser = p.chromium.launch(headless=True)
                context = browser.new_context()
                page = context.new_page()

                # Extract URL from task description
                url_match = re.search(r'https?://[^\s<>"]+|www\.[^\s<>"]+', task_description)
                if url_match:
                    url = url_match.group()
                    
                    event_system.notify_step(
                        thought=f"Navigating to {url}",
                        action="Page Load",
                        input_data=url,
                        observation="Loading webpage"
                    )

                    # Navigate to the page
                    page.goto(url)
                    page.wait_for_load_state('networkidle')

                    # Get page content
                    content = page.content()
                    soup = BeautifulSoup(content, 'html.parser')

                    # Remove script and style elements
                    for script in soup(["script", "style"]):
                        script.decompose()

                    # Extract text
                    text = soup.get_text()
                    lines = (line.strip() for line in text.splitlines())
                    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                    text = ' '.join(chunk for chunk in chunks if chunk)

                    # Close browser
                    browser.close()

                    # Add citation
                    event_system.notify_citation(
                        source=page.title(),
                        url=url,
                        content=text[:500] + "..."  # First 500 chars as preview
                    )

                    event_system.notify_step(
                        thought="Completed browser task",
                        action="Content Extraction",
                        input_data=url,
                        observation=f"Successfully extracted {len(text)} characters of content"
                    )

                    return text
                else:
                    error_msg = "No URL found in task description"
                    event_system.notify_step(
                        thought="Task failed",
                        action="URL Extraction",
                        input_data=task_description,
                        observation=error_msg
                    )
                    return error_msg

        except Exception as e:
            error_msg = f"Error during browser task: {str(e)}"
            event_system.notify_step(
                thought="Task failed",
                action="Browser Error",
                input_data=task_description,
                observation=error_msg
            )
            return error_msg

# # --- Optional: Example Usage for Testing ---
# # Uncomment the block below to test the tool directly.
# # Ensure Ollama is running and playwright browsers are installed (`playwright install chromium`).
# if __name__ == '__main__':
#     print("Testing BrowserTool...")
#     tool = BrowserTool()
#     # Example task:
#     test_task = "Go to duckduckgo.com and search for 'latest news on large language models'"
#     # test_task = "What is the main content on playwright.dev?"

#     try:
#         output = tool.run(test_task) # Use the public run method
#         print("\n===== Browser Tool Test Output =====")
#         print(output)
#         print("===================================")
#     except Exception as e:
#         print(f"Error during test execution: {e}")
#         import traceback
#         traceback.print_exc()
# # --- End Example Usage ---
