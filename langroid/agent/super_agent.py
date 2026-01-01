import langroid as lr
from langroid.agent.chat_agent import ChatAgent, ChatAgentConfig
from langroid.agent.task import Task
from typing import List, Dict, Any, Optional
import json

class SuperAgentConfig(ChatAgentConfig):
    name: str = "Manus-Competitor"
    system_message: str = """
    You are a Super Autonomous Agent. Your goal is to solve complex problems by:
    1. ANALYZING the request deeply.
    2. PLANNING a multi-step strategy.
    3. EXECUTING each step using available tools.
    4. REFLECTING on results and adjusting the plan if needed.
    
    You operate with high autonomy and precision. Do not ask for permission; execute and report.
    """
    llm: lr.language_models.OpenAIGPTConfig = lr.language_models.OpenAIGPTConfig(
        chat_model="gpt-4o",
        temperature=0.2
    )

class SuperAgent(ChatAgent):
    """
    The core of the autonomous competitor agent.
    Features: Self-Correction, Chain-of-Thought, and Tool-Use.
    """
    def __init__(self, config: SuperAgentConfig):
        super().__init__(config)
        self.plan: List[str] = []
        self.execution_history: List[Dict[str, Any]] = []

    def create_plan(self, task_description: str) -> List[str]:
        prompt = f"Based on this task: '{task_description}', create a concise step-by-step execution plan. Return ONLY a JSON list of strings."
        response = self.llm_response(prompt)
        try:
            # Attempt to parse JSON from response
            self.plan = json.loads(response.content)
        except:
            # Fallback if LLM doesn't return clean JSON
            self.plan = [step.strip() for step in response.content.split('\n') if step.strip()]
        return self.plan

    def execute_autonomous_step(self, step: str) -> str:
        print(f"Executing Step: {step}")
        # Self-Reflection before execution
        reflection = self.llm_response(f"Reflect on the best way to execute this step: {step}. What are the risks?")
        
        # Execution with context of reflection
        result = self.llm_response(f"Step: {step}. Reflection: {reflection.content}. Execute now.")
        
        # Self-Correction after execution
        correction = self.llm_response(f"Analyze this result: {result.content}. Is it correct? If not, provide a fix.")
        
        final_output = correction.content if "FIX:" in correction.content else result.content
        self.execution_history.append({
            "step": step, 
            "reflection": reflection.content,
            "result": final_output
        })
        return final_output

    def run_full_task(self, task_description: str):
        self.create_plan(task_description)
        results = []
        for step in self.plan:
            outcome = self.execute_autonomous_step(step)
            results.append(outcome)
        
        final_summary = self.llm_response(f"Summarize the full execution of: {task_description}. Steps taken: {json.dumps(self.execution_history)}")
        return final_summary.content
