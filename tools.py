from langchain.utilities import BingSearchAPIWrapper
from langchain.agents import Tool
import os
from dotenv import load_dotenv

load_dotenv()

search = BingSearchAPIWrapper(bing_subscription_key=os.environ["BING_SUBSCRIPTION_KEY"])

tools = [
    Tool(
        name = "Web Search",
        func=search.run,
        description="Useful for when you need to answer questions about travel destinations, weather, itinerary, etc."
    ),
]

tool_names = [tool.name for tool in tools]