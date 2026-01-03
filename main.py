from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import DeepLake
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaLLM
from langchain_classic.chains.retrieval_qa.base import RetrievalQA

from langchain_classic.agents import initialize_agent, Tool
from langchain_classic.agents import AgentType

import os
from dotenv import load_dotenv

# This reads the .env file and loads the variables
load_dotenv()
# Initialize Ollama model
model_name = os.getenv("OLLAMA_ML_MODEL")
# Get Deep Lake token from environment variable
# Deep lake is a Vector database/store by Activeloop
deep_lake_token = os.getenv("DEEP_LAKE_TOKEN")
deep_lake_org_name = os.getenv("DEEP_LAKE_ORG_NAME")
# Get Ollama embeddings model from environment variable
embeddings_model_name = os.getenv("OLLAMA_EMBEDDINGS_MODEL")
# Initialize Ollama model
llm = OllamaLLM(model=model_name, temperature=0.1)
embeddings_model = OllamaEmbeddings(model=embeddings_model_name)

# create/load Deep Lake dataset
my_activeloop_dataset_name = "langchain_course_from_zero_to_hero"
dataset_path = f"hub://{deep_lake_org_name}/{my_activeloop_dataset_name}"
db = DeepLake(dataset_path=dataset_path, embedding=embeddings_model, token=deep_lake_token)

# create our documents
texts = [
    "Lady Gaga was born in 28 March 1986",
    "Michael Jeffrey Jordan was born in 17 February 1963"
]

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.create_documents(texts)


# add documents to the database
db.add_documents(docs)

# RetrievalQA chain
retrieval_qa = RetrievalQA.from_chain_type(
	llm=llm,
	chain_type="stuff",
	retriever=db.as_retriever()
)

# create an agent that uses the RetrievalQA chain as a tool:
tools = [
    Tool(
        name="Retrieval QA System",
        func=retrieval_qa.run,
        description="Useful for answering questions about historical figures and dates."
    ),
]



# FIX: Added a custom error message to guide the Llama model when it formats incorrectly
agent = initialize_agent(
	tools,
	llm,
	agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
	verbose=True,
    # This specific string helps the model recover if it forgets "Action Input:"
	handle_parsing_errors="Invalid format. You must strictly use the format: Action: [Tool Name] and then Action Input: [Input]. Do not use 'Input:'."
)
# verbose=True: when set to True, 
# it will cause the Agent to print more detailed information about what it's doing. 
# This is useful for debugging and understanding what's happening under the hood

# Ensure the agent's execution adheres to the expected format
# Run the agent using invoke
response = agent.invoke({"input": "When was Michael Jordan born?"})

# Ensure the response is properly formatted and handle errors gracefully
if isinstance(response, dict) and "output" in response:
    print(response["output"])
else:
    print("Error: Unexpected response format.")