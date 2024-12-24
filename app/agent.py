import logging
from typing import Optional

import requests
from pydantic import BaseModel, Field
from pydantic_ai import Agent, Tool

import rag
from config import settings

logger = logging.getLogger(__name__)


def read_file(file_path: str):
    with open(file_path, "r") as file:
        return file.read()


def initialize_agent():
    agent_system_prompt = read_file(f"{settings.RESOURCES_PATH}/prompts/system_prompt.MD")
    agent = Agent(model="openai:gpt-4o",
                  system_prompt=agent_system_prompt,
                  tools=[Tool(name="query_knowledge_base", function=rag.query, takes_ctx=False,
                              description="useful for when you need to answer questions about service information or services offered, availability and their costs.")])

    @agent.tool_plain
    async def get_cost_estimate(issue: str, plumbing_type: str) -> str:
        """Estimate the cost of cleaning a property based on the plumbing issue and property type."""
        system_prompt = read_file(f"{settings.RESOURCES_PATH}/prompts/cost_estimator_prompt.MD").format(issue=issue, plumbing_type=plumbing_type)

        cost_agent = Agent("openai:gpt-4o", system_prompt=system_prompt)
        response = await cost_agent.run(" ", model_settings={"temperature": 0.2})
        print(response.cost())
        print(response.data)
        return response.data

    class ServiceRequest(BaseModel):
        name: str = Field(description="Full name of the lead")
        phone_number: str = Field(description="Contact phone number")
        email: str = Field(description="Email address")
        description: Optional[str] = Field(description="Additional description", default="")

    @agent.tool_plain
    async def register_service_request(request: ServiceRequest):
        """Registers a new service request in Airtable."""
        base_url: str = "https://api.airtable.com"
        api_key: str = settings.AIRTABLE_API_KEY
        base_id: str = settings.AIRTABLE_BASE_ID
        url = f"{base_url}/v0/{base_id}/FlowFix"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "fields": {
                "Name": request.name,
                "Phone": request.phone_number,
                "Email": request.email,
                "Description": request.description
            }
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()

            return {
                "status": "success",
                "data": response.json()
            }
        except requests.RequestException as e:
            return {
                "status": "error",
                "error": str(e),
                "details": response.text if hasattr(response, 'text') else None
            }
    return agent


agent = initialize_agent()
chat_histories = {}


async def test():
    messages = []
    while True:
        query = input("You: ")
        if query.lower() in ['quit', 'exit', 'bye']:
            break

        response = await agent.run(query, message_history=messages)
        print("Agent:", response.data)
        messages = response.all_messages()


async def handle_user_message(user_id: str, message: str):
    if user_id not in chat_histories:
        chat_histories[user_id] = []
    messages = chat_histories[user_id]
    response = await agent.run(message, message_history=messages)
    logger.info(f"Agent: {response.data}")
    messages = response.all_messages()
    chat_histories[user_id] = messages
    return response

# import asyncio
# asyncio.run(handle_user_message(user_id="1", message="How much to fix a pipe?"))

logger.info("Agent initialized.")
