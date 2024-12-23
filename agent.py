from typing import Optional

import requests
from pydantic import BaseModel, Field
from pydantic_ai import Agent, Tool

import rag
from config import settings


def read_file(file_path: str):
    with open(file_path, "r") as file:
        return file.read()


agent_system_prompt = read_file(f"{settings.RESOURCES_PATH}/prompts/system_prompt.MD")

simple_agent = Agent(model="openai:gpt-4o", system_prompt=agent_system_prompt)
# response = simple_agent.run_sync("who are you", model_settings={"temperature": 0.0})
# print(response.data)
# print(response.cost())
# print(response.all_messages())


agent = Agent(model="openai:gpt-4o",
              system_prompt=agent_system_prompt,
              tools=[Tool(name="query_knowledge_base", function=rag.query, takes_ctx=False,
                          description="useful for when you need to answer questions about service information or services offered, availability and their costs.")])

# response = agent.run_sync("how much to fix pipe for residential property?")
# print(response.data)
# print(response.cost())
# print(response.all_messages())


@agent.tool_plain
async def get_cost_estimate(issue: str, plumbing_type: str) -> str:
    system_prompt = read_file(f"{settings.RESOURCES_PATH}/prompts/cost_estimator_prompt.MD").format(issue=issue, plumbing_type=plumbing_type)
    """Estimate the cost of cleaning a property based on the plumbing issue and property type."""

    cost_agent = Agent("openai:gpt-4o", system_prompt=system_prompt)
    response = await cost_agent.run(" ", model_settings={"temperature": 0.2})
    print(response.cost())
    print(response.data)
    return response.data

#
# response = agent.run_sync("what's the cost estimates", message_history=response.all_messages())
# print(response.data)
# print(response.cost())


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

# import asyncio
# asyncio.run(register_service_request(ServiceRequest(name="John Doe", phone_number="1234567890", email="test@mail.com", description="This is a test request")))
