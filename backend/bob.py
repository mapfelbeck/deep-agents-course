### Netskope workaround ###
import truststore
truststore.inject_into_ssl()
##########################
from deepagents import create_deep_agent
from models import openai

agent = create_deep_agent(model=openai)

result = agent.invoke({"messages": [{"role": "user", "content": "What is an LLM?"}]})

print(result["messages"][-1].content)
