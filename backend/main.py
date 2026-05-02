# backend/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.agents import PlanningAgentManager

app = FastAPI(title="AI Personal Planning Assistant API")
agent_manager = PlanningAgentManager()

class PlanRequest(BaseModel):
    user_input: str

@app.get("/")
def read_root():
    return {"message": "AI Personal Planning Assistant API is running"}

@app.post("/plan")
async def create_plan(request: PlanRequest):
    try:
        result = agent_manager.run_full_chain(request.user_input)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
