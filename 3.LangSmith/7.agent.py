from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
import requests
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_classic import hub
from dotenv import load_dotenv

load_dotenv()

search_tool = DuckDuckGoSearchRun()

@tool
def get_weather_data(city: str) -> float:
  """
  This function fetches the current weather data for a given city
  """
  import requests

  geo = requests.get(
      "https://geocoding-api.open-meteo.com/v1/search",
      params={"name": city, "count": 1}
  ).json()

  lat = geo["results"][0]["latitude"]
  lon = geo["results"][0]["longitude"]

  weather = requests.get(
      "https://api.open-meteo.com/v1/forecast",
      params={
          "latitude": lat,
          "longitude": lon,
          "current_weather": True
      }
  ).json()

  return weather['current_weather']['temperature']

llm = ChatOpenAI()

# Step 2: Pull the ReAct prompt from LangChain Hub
prompt = hub.pull("hwchase17/react")  # pulls the standard ReAct agent prompt

# Step 3: Create the ReAct agent manually with the pulled prompt
agent = create_react_agent(
    llm=llm,
    tools=[search_tool, get_weather_data],
    prompt=prompt
)

# Step 4: Wrap it with AgentExecutor
agent_executor = AgentExecutor(
    agent=agent,
    tools=[search_tool, get_weather_data],
    verbose=True,
    max_iterations=5
)

# What is the release date of Dhadak 2?
# What is the current temp of gurgaon
# Identify the birthplace city of Kalpana Chawla (search) and give its current temperature.

# Step 5: Invoke
response = agent_executor.invoke({"input": "Identify the birthplace city of Kalpana Chawla (search) and give its current temperature"})

print(response)
print(response['output'])