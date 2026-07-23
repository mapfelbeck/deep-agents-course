### Netskope workaround ###
import truststore
truststore.inject_into_ssl()
###########################
from deepagents import create_deep_agent
from models import openai
from confluence_tool import import_confluence

agent = create_deep_agent(
    model=openai,
    tools=[import_confluence],
    system_prompt=(
        "You are a helpful assistant that imports Confluence documentation. "
        "When asked to import the confluence data, call the import_confluence tool."
    ),
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "Import the confluence data."}]}
)

print(result["messages"][-1].content)
