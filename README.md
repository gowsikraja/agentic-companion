
# 🤖 LangGraph Agent Chat

This project is a chatbot application built with Streamlit and LangGraph. It uses a Large Language Model (LLM) from Google (specifically, Gemini) to power the chat functionality. The agent is equipped with tools to perform specific tasks like multiplication and squaring numbers.

## ✨ Features

*   Interactive chat interface built with Streamlit.
*   Powered by Google's Gemini LLM.
*   Extensible with custom tools.
*   Clear and modular project structure.

## 📂 File Structure


Here's a breakdown of the important files in this project:

| File                | Description                                                                                                                              |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `app/app.py`        | The main entry point. The Streamlit application creates the user interface for the chatbot, manages the chat history, and interacts with the `ChatAgent`.     |
| `app/agent.py`      | The core of the application. It defines the `ChatAgent` class, which encapsulates the LangGraph agent.                                   |
| `app/config.py`     | Handles the configuration for the application, such as loading the `GOOGLE_API_KEY` from a `.env` file and setting the model name.         |
| `app/tools.py`      | Defines the tools that the agent can use. In this case, it defines `multiply` and `square` functions.                                      |
| `requirement.txt`   | Lists the Python dependencies for this project.                                                                                          |
| `pyproject.toml`    | Specifies the project metadata and dependencies.                                                                                         |


## �️ Screenshot

<img src="https://raw.githubusercontent.com/gowsikraja/agentic-companion/refs/heads/main/Screenshot.png" alt="LangGraph Agent Chat Screenshot" width="700"/>

## �🚀 Getting Started

Follow these steps to get the project up and running on your local machine.

### Prerequisites

*   Python 3.13 or higher
*   Pip

### 1. Clone the repository

```bash
git clone https://github.com/gowsikraja/agentic-companion.git
cd agentic-companion
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirement.txt
```

### 4. Set up your environment variables

Create a `.env` file in the root directory of the project and add your Google API key:

```
GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"
```


### 5. Run the application

```bash
streamlit run app/app.py
```

Now, you can open your browser and navigate to `http://localhost:8501` to interact with the chatbot.

---

## 🛣️ Upcoming Features

We're planning to add the following features soon:

1. Get API key at runtime from the user (no need to edit .env)
2. Support for different LLM models (selectable by user)
3. Enable/disable multiple tools dynamically
4. Multimodal support: audio, image, video, and document input/output

---

## 🤝 Contributing


We love contributions! 🚀 Whether it's a bug fix, feature suggestion, or a new tool/model integration, your input is welcome. Check out the issues or open a pull request to get started. Let's build something amazing together!

## 📝 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
