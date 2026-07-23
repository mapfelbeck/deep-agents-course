### Netskope workaround ###
import truststore
truststore.inject_into_ssl()
##########################
from deepagents import create_deep_agent
from models import openai

confluence_import_location = "imported"
confluence_doc_id = 56819899

agent = create_deep_agent(model=openai)

result = agent.invoke({"messages": [{"role": "user", "content": "What is an LLM?"}]})

print(result["messages"][-1].content)
