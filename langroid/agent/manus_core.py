import subprocess
import sys
import os
from typing import Dict, Any, List
import langroid as lr
from langroid.agent.super_agent import SuperAgent, SuperAgentConfig

class ManusCloneConfig(SuperAgentConfig):
    name: str = "Manus-Clone-X"
    system_message: str = """
    You are Manus-Clone-X, the ultimate autonomous AI. 
    Your core capability is SELF-PROGRAMMING. 
    If you don't have a tool, WRITE one in Python and EXECUTE it.
    You have full access to the shell and environment.
    Solve any problem by writing code, running it, and iterating until success.
    """

class ManusCore(SuperAgent):
    """
    The 'Nervous System' of the project. 
    Enables self-coding and live execution.
    """
    def execute_python_code(self, code: str) -> str:
        """Executes python code and returns output."""
        try:
            # Safety: In a real enterprise app, this would be sandboxed.
            # For this clone, we give it full power.
            with open("temp_script.py", "w") as f:
                f.write(code)
            result = subprocess.run([sys.executable, "temp_script.py"], capture_output=True, text=True, timeout=30)
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return str(e)

    def solve_with_code(self, task: str):
        """The Manus way: Think -> Code -> Execute -> Result."""
        plan = self.create_plan(task)
        for step in plan:
            code_prompt = f"Write a Python script to achieve this step: {step}. Return ONLY the code."
            code = self.llm_response(code_prompt).content
            # Clean code from markdown if present
            code = code.replace("```python", "").replace("```", "").strip()
            
            print(f"Manus-Clone is coding for step: {step}")
            output = self.execute_python_code(code)
            print(f"Execution Output: {output}")
            
            self.execution_history.append({"step": step, "code": code, "output": output})
        
        return self.llm_response(f"Task complete. Summary of all code executions: {self.execution_history}").content
