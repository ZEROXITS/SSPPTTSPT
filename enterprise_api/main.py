import os
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import langroid as lr
import langroid.language_models as lm
from langroid.agent.chat_agent import ChatAgent, ChatAgentConfig
from langroid.agent.super_agent import SuperAgent, SuperAgentConfig
from langroid.agent.manus_core import ManusCore, ManusCloneConfig
from langroid.agent.task import Task
import uvicorn

app = FastAPI(title="Langroid Enterprise API", version="1.0.0")

# In-memory storage for active tasks and agents (for demo purposes)
# In production, this would be in Redis/PostgreSQL
active_agents = {}
active_tasks = {}

class AgentConfigModel(BaseModel):
    name: str
    system_message: str
    model: str = "gpt-4o"
    use_tools: bool = True

class ChatRequest(BaseModel):
    agent_id: str
    message: str

class ChatResponse(BaseModel):
    response: str
    usage: Optional[Dict[str, Any]] = None

@app.post("/agents/create")
async def create_agent(config: AgentConfigModel):
    try:
        llm_cfg = lm.OpenAIGPTConfig(chat_model=config.model)
        agent_cfg = ChatAgentConfig(
            name=config.name,
            system_message=config.system_message,
            llm=llm_cfg
        )
        agent = ChatAgent(agent_cfg)
        agent_id = f"agent_{len(active_agents) + 1}"
        active_agents[agent_id] = agent
        return {"agent_id": agent_id, "status": "created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat_with_agent(request: ChatRequest):
    if request.agent_id not in active_agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    agent = active_agents[request.agent_id]
    try:
        response = agent.llm_response(request.message)
        return ChatResponse(
            response=response.content,
            usage=response.usage if hasattr(response, 'usage') else None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/super-agent/run")
async def run_super_agent(task: str):
    try:
        config = SuperAgentConfig()
        agent = SuperAgent(config)
        result = agent.run_full_task(task)
        return {
            "task": task,
            "result": result,
            "plan": agent.plan,
            "history": agent.execution_history
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/manus/solve")
async def manus_solve(task: str):
    try:
        config = ManusCloneConfig()
        agent = ManusCore(config)
        result = agent.solve_with_code(task)
        return {
            "agent": "Manus-Clone-X",
            "task": task,
            "final_solution": result,
            "execution_log": agent.execution_history
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
