# 🔍 CrewAI Browser Researcher

A powerful research assistant that leverages CrewAI to perform comprehensive web research, analysis, and fact-checking using local Ollama models.

## 🌟 Features

- **Multi-Agent Research System**
  - Web Research Specialist: Performs deep web searches and gathers information
  - Content Analyzer: Analyzes and synthesizes research findings
  - Fact Checker: Verifies information accuracy and reliability

- **Real-Time Research Visualization**
  - Live progress tracking of research steps
  - Detailed citation tracking
  - Research process statistics
  - Beautiful Gradio interface

- **Local AI Processing**
  - Powered by Ollama for local model inference
  - Configurable model selection
  - Privacy-focused research

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Ollama installed and running locally
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/crewai_Deep_researcher.git
cd crewai-Deep-researcher
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
Create a `.env` file in the project root with:
```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2
```

### Running the Application

1. Start the Gradio interface:
```bash
python src/visualizer.py
```

2. Open your browser and navigate to the URL shown in the terminal (typically http://localhost:7860)

## 🛠️ Project Structure

```
crewai-browser-researcher/
├── src/
│   ├── agents.py          # Agent definitions and configurations
│   ├── tasks.py           # Task definitions and execution logic
│   ├── event_system.py    # Event handling system
│   └── visualizer.py      # Gradio interface implementation
├── requirements.txt       # Project dependencies
├── .env                  # Environment variables
└── README.md            # This file
```

## 🔧 Configuration

### Agents

The project uses three specialized agents:

1. **Web Research Specialist**
   - Performs web searches
   - Gathers relevant information
   - Tracks sources and citations

2. **Content Analyzer**
   - Analyzes research findings
   - Identifies key insights
   - Synthesizes information

3. **Fact Checker**
   - Verifies information accuracy
   - Cross-references sources
   - Validates conclusions

### Ollama Configuration

The project uses Ollama for local model inference. You can configure:

- Model selection in `.env`
- Base URL for Ollama API
- Model parameters in `src/agents.py`

## 📝 Usage

1. Enter your research query in the Gradio interface
2. Watch the research process in real-time:
   - Research steps
   - Citations
   - Analysis progress
3. View the final comprehensive report including:
   - Initial research findings
   - Analysis results
   - Fact-checking verification

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [CrewAI](https://github.com/joaomdmoura/crewAI) for the multi-agent framework
- [Ollama](https://ollama.ai/) for local model inference
- [Gradio](https://gradio.app/) for the beautiful interface

## 📞 Support

For support, please open an issue in the GitHub repository or contact the maintainers.

## 🔄 Updates

- **v1.0.0**: Initial release with basic research capabilities
- **v1.1.0**: Added real-time visualization and improved UI
- **v1.2.0**: Integrated Ollama for local model support

## 📚 Documentation

For detailed documentation, please visit our [Wiki](https://github.com/yourusername/crewai-browser-researcher/wiki).
