import asyncio
from agent import agent


async def local_test():
    messages = []
    while True:
        query = input("You: ")
        if query.lower() in ['quit', 'exit', 'bye']:
            break

        response = await agent.run(query, message_history=messages)
        print("Agent:", response.data)
        messages = response.all_messages()


if __name__ == "__main__":
    asyncio.run(local_test())