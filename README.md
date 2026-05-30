# Docker Assistant Agent

A lightweight Agentic AI project built using LangChain, Ollama, and Docker. The agent interacts with Docker through natural language commands and performs container management tasks using custom tools.

## Features

- List all Docker containers
- List running Docker containers
- Count running containers
- List available Docker images
- Get detailed container information

## Tech Stack

- Python
- LangChain
- Ollama (Qwen 2.5 1.5B)
- Docker

## Project Structure

```
Docker-Assistant-Agent/
│
├── agent.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation

### Clone the Repository

```bash
git clone https://github.com/02Tirtha/Docker-Assistant-Agent.git
cd Docker-Assistant-Agent
```

### Create Virtual Environment

```bash
python -m venv agentenv
```

### Activate Environment

Windows:

```bash
agentenv\Scripts\activate
```

Linux/Mac:

```bash
source agentenv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Prerequisites

- Docker Desktop installed and running
- Ollama installed

Pull the model:

```bash
ollama pull qwen2.5:1.5b
```

## Run the Agent

```bash
python agent.py
```

## Example Commands

```text
show docker images

list all containers

show running containers

count running containers

show details of expenseapp
```

## Sample Output

```text
What do you want to ask the agent?: show running containers

expenseapp
mysql
```

## Limitations

- Uses a small local model (Qwen 2.5 1.5B), which may occasionally hallucinate or misinterpret tool outputs.
- Designed for learning Agentic AI and Docker tool integration.

## Future Improvements

- Run new Docker containers from images
- Build Docker images from Dockerfiles
- Remove containers/images
- Docker Compose support
- Web-based UI using Streamlit

## Author

Tirtha Jhaveri
