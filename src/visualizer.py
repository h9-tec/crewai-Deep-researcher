import gradio as gr
from datetime import datetime
import json
from typing import Dict, Any, List
from crewai import Crew
from event_system import event_system
from agents import web_research_specialist, content_analyzer, fact_checker
from tasks import get_research_task, get_analysis_task, get_fact_checking_task

class ResearchVisualizer:
    def __init__(self):
        self.chat_history = []
        self.research_steps = []
        self.citations = []
        self.start_time = None
        self.current_thought = ""
        self.current_action = ""
        self.current_observation = ""
        
        # Subscribe to events
        event_system.subscribe_to_step(self.update_step)
        event_system.subscribe_to_citation(self.update_citation)
        event_system.subscribe_to_message(self.update_message)

    def update_step(self, thought, action, input_data, observation):
        """Update research step information"""
        self.current_thought = thought
        self.current_action = action
        self.current_observation = observation
        step = {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "thought": thought,
            "action": action,
            "input": input_data,
            "observation": observation
        }
        self.research_steps.append(step)
        return self.format_research_steps()  # Return updated steps for real-time display

    def update_citation(self, title, url, content):
        """Update citation information"""
        citation = {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "title": title,
            "url": url,
            "content": content
        }
        self.citations.append(citation)
        return self.format_citations()  # Return updated citations for real-time display

    def update_message(self, role, content):
        """Update chat message"""
        self.chat_history.append((role, content))
        return self.format_chat_history()  # Return updated chat history for real-time display

    def format_chat_history(self):
        """Format chat history for Gradio"""
        formatted_history = []
        for role, content in self.chat_history:
            if role == "user":
                formatted_history.append([content, None])
            else:
                if formatted_history and formatted_history[-1][1] is None:
                    formatted_history[-1][1] = content
                else:
                    formatted_history.append([None, content])
        return formatted_history

    def format_research_steps(self):
        """Format research steps for display"""
        if not self.research_steps:
            return "No research steps yet."
        
        steps_text = "🔍 Research Process:\n\n"
        for step in self.research_steps:
            steps_text += f"[{step['timestamp']}] 🤖 {step['action']}\n"
            steps_text += f"💭 Thought: {step['thought']}\n"
            if step['input']:
                steps_text += f"📥 Input: {step['input']}\n"
            steps_text += f"📝 Observation: {step['observation']}\n\n"
        return steps_text

    def format_citations(self):
        """Format citations for display"""
        if not self.citations:
            return "No citations yet."
        
        citations_text = "📚 Citations:\n\n"
        for citation in self.citations:
            citations_text += f"[{citation['timestamp']}] 📄 {citation['title']}\n"
            citations_text += f"🔗 URL: {citation['url']}\n"
            citations_text += f"📝 Content: {citation['content']}\n\n"
        return citations_text

    def get_research_summary(self):
        """Get research summary statistics"""
        if not self.start_time:
            return "Research not started yet."
        
        duration = datetime.now() - self.start_time
        return f"""
        📊 Research Summary:
        - Total Steps: {len(self.research_steps)}
        - Citations Collected: {len(self.citations)}
        - Time Elapsed: {duration.seconds // 60}m {duration.seconds % 60}s
        """

def run_research_process(query, history):
    """Run the research process and update the interface"""
    if not query:
        return history, "", "", ""
    
    # Initialize research
    visualizer = ResearchVisualizer()
    visualizer.start_time = datetime.now()
    
    # Add initial message
    event_system.notify_message("user", query)
    event_system.notify_message("assistant", "🔍 Starting research process...")
    
    try:
        # 1. Research Task
        research_task = get_research_task(query)
        research_crew = Crew(
            agents=[web_research_specialist],
            tasks=[research_task],
            process="sequential",
            verbose=True
        )
        research_output = research_crew.kickoff()
        event_system.notify_message("assistant", f"📝 Research Findings:\n\n{research_output}")
        
        # 2. Analysis Task with research results as input
        analysis_task = get_analysis_task(research_output)
        analysis_crew = Crew(
            agents=[content_analyzer],
            tasks=[analysis_task],
            process="sequential",
            verbose=True
        )
        analysis_output = analysis_crew.kickoff()
        event_system.notify_message("assistant", f"🔍 Analysis Results:\n\n{analysis_output}")
        
        # 3. Fact Checking Task with analysis results as input
        fact_checking_task = get_fact_checking_task(analysis_output)
        fact_checking_crew = Crew(
            agents=[fact_checker],
            tasks=[fact_checking_task],
            process="sequential",
            verbose=True
        )
        final_output = fact_checking_crew.kickoff()
        
        # Add final comprehensive result
        final_summary = f"""
        🎯 Final Research Results:
        
        1️⃣ Initial Research:
        {research_output}
        
        2️⃣ Analysis:
        {analysis_output}
        
        3️⃣ Fact Check:
        {final_output}
        """
        event_system.notify_message("assistant", final_summary)
        
    except Exception as e:
        error_msg = f"❌ An error occurred: {str(e)}"
        event_system.notify_message("assistant", error_msg)
        print(f"Error details: {e}")
    
    # Format and return updated interface components
    formatted_history = visualizer.format_chat_history()
    steps_text = visualizer.format_research_steps()
    citations_text = visualizer.format_citations()
    summary_text = visualizer.get_research_summary()
    
    return formatted_history, steps_text, citations_text, summary_text

def create_gradio_interface():
    """Create the Gradio interface"""
    with gr.Blocks(theme=gr.themes.Soft()) as interface:
        gr.Markdown("# 🔍 Deep Research Assistant")
        gr.Markdown("Ask any question and get comprehensive research results with citations.")
        
        with gr.Row():
            with gr.Column(scale=2):
                chatbot = gr.Chatbot(
                    [],
                    elem_id="chatbot",
                    height=500,
                    show_label=False
                )
                query = gr.Textbox(
                    placeholder="Enter your research question...",
                    show_label=False
                )
                clear = gr.Button("Clear")
            
            with gr.Column(scale=1):
                with gr.Tab("Research Steps"):
                    steps_display = gr.Textbox(
                        value="No research steps yet.",
                        label="Research Process",
                        lines=20,
                        max_lines=30
                    )
                with gr.Tab("Citations"):
                    citations_display = gr.Textbox(
                        value="No citations yet.",
                        label="Sources and Citations",
                        lines=20,
                        max_lines=30
                    )
                with gr.Tab("Summary"):
                    summary_display = gr.Textbox(
                        value="Research not started yet.",
                        label="Research Summary",
                        lines=10
                    )
        
        # Set up event handlers
        query.submit(
            run_research_process,
            [query, chatbot],
            [chatbot, steps_display, citations_display, summary_display]
        )
        
        clear.click(
            lambda: ([], "", "", ""),
            None,
            [chatbot, steps_display, citations_display, summary_display],
            queue=False
        )
    
    return interface

if __name__ == "__main__":
    interface = create_gradio_interface()
    interface.launch(share=False) 