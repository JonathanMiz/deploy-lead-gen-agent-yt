from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from mangum import Mangum

from config import settings
import agent

app = FastAPI(title="Website Lead Generation Agent")
handler = Mangum(app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Change this to the actual domain of the website
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
@app.get("/health")
def check_health():
    return {"status": "ok"}


@app.get("/call-agent")
async def call_agent(request: Request):
    query = request.query_params.get("query")
    user_id = request.query_params.get("user_id")
    if not query:
        raise HTTPException(status_code=400, detail="Query parameter is required.")
    response = await agent.handle_user_message(user_id=user_id, message=query)
    return response.data


if __name__ == "__main__":
    port = settings.PORT
    print(f"Running the FastAPI server on port {port}.")
    uvicorn.run("api:app", host="0.0.0.0", port=port)
