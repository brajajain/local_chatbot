# Local Chatbot
A ChatGPT style app for a local LLM

# Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.11 or newer.
- Poetry for Python package and dependency management. If you do not have Poetry installed, follow the [installation instructions on Poetry's website](https://python-poetry.org/docs/#installation).
- Ollama | [click to download](https://ollama.ai/download)
    - install and run `ollama run mixtral`

# Installation
1. **Clone the repository**:
```bash
   git clone https://github.com/brajajain/local_chatbot.git
```

 
2. **Upgrade pip** 
Ensure you have the latest version of pip by running:
```sh
pip install --upgrade pip
``` 

3. **Install Poetry** 
Poetry is used for dependency management and packaging. Install it by running:
```sh
pip install poetry
```

4. **Activate your virtual environment** 
With Poetry installed, navigate to the root of the `local_chatbot` project directory (where the `pyproject.toml` is located) and run:
```sh
poetry shell
``` 


5. **Install `local_chatbot` Dependencies** 
```sh
poetry install
``` 

# Usage
**Run the Chatbot** 
```sh
chainlit run chat/chat.py
```
