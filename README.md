
# Lead Generation AI Agent

This is the code for the "Build a Lead Generation AI Agent" tutorial on [YouTube](https://youtu.be/RGEJhcWdXR4).

## Technology Stack and Features

- [**Python**](https://www.python.org) for the logic.
- [**PydanticAI**](https://ai.pydantic.dev/) for the AI agent framework.
- [**Chroma**](https://www.trychroma.com/) for the vector database.
- [**OpenAI**](https://platform.openai.com/) for the AI model.
- [**Airtable**](https://airtable.com/) for the database.

## How To Use It


### Clone the repository

```bash
git clone https://github.com/JonathanMiz/deploy-lead-gen-agent-yt.git

cd lead-gen-agent-yt
```

### Create a virtual environment

```bash
python3 -m venv .venv
```

### Activate virtual environment

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip3 install -r requirements.txt
```

### Add API keys

Create a file called `.env` in the root directory and add the following:

```
OPENAI_API_KEY=your-api-key

AIRTABLE_API_KEY=your-api-key

AIRTABLE_BASE_ID=your-base-id
```

*Note: don't commit the `.env` file to the repository.*

To get an OpenAI API key, visit [OpenAI](https://platform.openai.com/).

To get an Airtable API key, visit [Airtable](https://airtable.com/account).

### Build the vector database

```bash
python3 build_vector_db.py
```

### Query the knowledge base

```bash
python3 rag.py --query "How much to fix pipe for residential property?"
```

### Run the AI agent

```bash
python3 main.py
```

### Watch the full step-by-step tutorial

[![Watch the tutorial](https://img.youtube.com/vi/RGEJhcWdXR4/sddefault.jpg)](https://youtu.be/RGEJhcWdXR4)