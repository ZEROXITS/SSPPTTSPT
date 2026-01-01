from typing import List, Optional, Dict, Any
import langroid as lr
from langroid.agent.chat_agent import ChatAgent
from langroid.agent.task import Task

class EnterpriseOrchestrator:
    """
    Advanced Orchestrator to manage complex multi-agent workflows.
    """
    def __init__(self, main_agent: ChatAgent):
        self.main_task = Task(main_agent, name="Orchestrator")
        self.sub_tasks = []

    def add_specialized_agent(self, agent: ChatAgent, name: str, system_message: str):
        """Adds a specialized sub-agent to the orchestration."""
        sub_task = Task(
            agent, 
            name=name, 
            system_message=system_message,
            single_round=True
        )
        self.main_task.add_sub_task(sub_task)
        self.sub_tasks.append(sub_task)

    def execute_workflow(self, initial_input: str):
        """Runs the entire multi-agent workflow."""
        return self.main_task.run(initial_input)

    def get_workflow_status(self):
        """Returns the current state of all agents in the workflow."""
        return {
            "main_agent": self.main_task.agent.config.name,
            "sub_agents": [t.name for t in self.sub_tasks],
            "status": "active"
        }
