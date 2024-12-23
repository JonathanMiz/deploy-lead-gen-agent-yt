import asyncio
from pydantic_ai import Agent
import chroma_db


async def query(question: str):
    db = chroma_db.get()
    retriever = db.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.5, "k": 3})
    documents = retriever.invoke(question)

    def format_docs(docs):
        return "\n\n ********* \n\n".join([d.page_content for d in docs])

    prompt_template = """Answer the question based only on the following context:

    {context}

    Question: {question}
    """
    prompt = prompt_template.format(context=format_docs(documents), question=question)

    query_agent = Agent("openai:gpt-4o")
    response = await query_agent.run(prompt, model_settings={'temperature': 0.0})
    print(response.cost())
    return response.data


async def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", type=str, help="Query to ask the RAG model")
    args = parser.parse_args()
    user_query = args.query
    if not args.query:
        print("Please provide a query to ask the RAG model.")
        return
    result = await query(user_query)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())