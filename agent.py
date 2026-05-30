from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama # to use the Ollama local model as the language model for the agent. This allows you to run the model on your local machine without needing an internet connection.
import subprocess # package to run shell commands from Python.
from langchain_core.tools import tool # to create tools that can be used by the agent, such as running shell commands or accessing APIs.
from langchain.agents import create_agent #to create an agent that can use the tools and the language model to perform tasks.

# 1. Initialize the local model
llm = ChatOllama(
    model="qwen2.5:1.5b", # qwen3:8b is a smaller model that can run on a local machine. You can also use "qwen3:14b" if you have more resources.
    # 5b means 5 billion parameters
    temperature=0.7, # randomness of the output, between 0 and 1. Higher values make the output more random, while lower values make it more deterministic.
)

# 2. Define your prompt structure
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that answers in exactly two sentences."),
    ("user", "{input}")
])

# 3. Combine components using a pipe (|) operator
chain = prompt | llm | StrOutputParser()


# 4. TOOL  --> Tools are functions that the agent can call to perform specific tasks. 

# To get the list of all Docker containers. 
@tool
def get_all_docker_containers():
    """Tool to get the list of all Docker containers."""
    try:
        output = subprocess.check_output(
            ["docker", "ps", "-a",  "--format", "{{.Names}}"]
        )

        return output.decode("utf-8")

    except Exception as e:
        return f"An error occurred: {e}"

# To get the list of running Docker containers.
@tool
def get_running_docker_containers():
    """Tool to get the list of running Docker containers."""
    try:
        # Run the Docker ps command and capture its output
        output = subprocess.check_output(
            ["docker", "ps", "--format", "{{.Names}}"]
        )

        return output.decode("utf-8") # return decoded output as a string

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# To count the number of running Docker containers.
@tool
def count_running_containers():
    """Count running Docker containers."""
    try:
        output = subprocess.check_output(
            ["docker", "ps", "-q"]
        )

        return str(
            len(output.decode().splitlines())
        )

    except Exception as e:
        return f"Error: {e}"

# To get the list of Docker images available on the system.        
@tool
def list_docker_images():
    """Get the list of Docker images available on the system."""
    try:
        output = subprocess.check_output(
            ["docker", "images", "--format", "{{.Repository}}:{{.Tag}}"]
        )

        return output.decode("utf-8")

    except Exception as e:
        return f"An error occurred: {e}"

# To get detailed information about a specific Docker container given its name.
@tool
def get_detailed_container_info(container_name: str):
    """Get detailed information about a Docker container."""
    try:
        output = subprocess.check_output(
            ["docker", "inspect", container_name]
        )

        return output.decode("utf-8")

    except Exception as e:
        return f"An error occurred: {e}"

# 5. Create an agent that can use the tool
agent = create_agent(
        model=llm, 
        tools=[
               get_all_docker_containers,
               list_docker_images,
               get_running_docker_containers,
               count_running_containers,
               get_detailed_container_info,
               ],
        system_prompt="""
            You are a helpful Docker assistant.
            Use list_docker_images to list available Docker images on the system.
            Use get_all_docker_containers to list all containers, including stopped ones.
            Use get_running_docker_containers to list running containers.
            Use count_running_containers to count the number of running containers.
            Use get_detailed_container_info to get detailed information about a specific container.
            Never claim success unless a tool explicitly returns SUCCESS.
            If a tool returns FAILED or an error message,
            inform the user that the operation failed and explain the error.
            Do not assume containers or images exist.
            """    
    )


# 6. Invoke the chain
print("""
==================================================
            Docker Assistant Agent
==================================================

I can help you with the following tasks:

1. List available Docker images
   Example: show docker images

2. List all Docker containers
   (including running and stopped containers)
   Example: show all containers

3. List running Docker containers
   Example: show running containers

4. Get detailed information about a container
   Example: show details of expenseapp

Type 'exit' to quit.

==================================================
""")

while True:
    question = input(f"\nWhat do you want to ask the agent?:")
 
    if question.lower() == "exit":
        print("Goodbye!")
        break

    response = agent.invoke({
        "messages": [("user", question)]  # we pass the user input as a message to the agent, which will then process it using the language model and the tool to generate a response.
    })

    print("\n=== Agent Response ===")
    print(response["messages"][-1].content)

    print("\n=== Tool Calls ===")
    for msg in response["messages"]:
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            print(msg.tool_calls)