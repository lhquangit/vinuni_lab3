import json
import os
import re
from typing import List, Dict, Any, Optional
from src.core.llm_provider import LLMProvider
from src.telemetry.logger import logger

class ReActAgent:
    """
    SKELETON: A ReAct-style Agent that follows the Thought-Action-Observation loop.
    Students should implement the core loop logic and tool execution.
    """
    
    def __init__(self, llm: LLMProvider, tools: List[Dict[str, Any]], max_steps: int = 5):
        self.llm = llm
        self.tools = tools
        self.max_steps = max_steps
        self.history = []

    def get_system_prompt(self) -> str:
        """
        TODO: Implement the system prompt that instructs the agent to follow ReAct.
        Should include:
        1.  Available tools and their descriptions.
        2.  Format instructions: Thought, Action, Observation.
        """
        tool_descriptions = "\n".join(
            [
                f"- {self._tool_attr(t, 'name')}: {self._tool_attr(t, 'description')}"
                for t in self.tools
            ]
        )
        return f"""
        You are an intelligent assistant. You have access to the following tools:
        {tool_descriptions}

        Use the following format:
        Thought: your line of reasoning.
        Action: tool_name(arguments)
        Observation: result of the tool call.
        ... (repeat Thought/Action/Observation if needed)
        Final Answer: your final response.
        """

    def run(self, user_input: str) -> str:
        """
        TODO: Implement the ReAct loop logic.
        1. Generate Thought + Action.
        2. Parse Action and execute Tool.
        3. Append Observation to prompt and repeat until Final Answer.
        """
        logger.log_event("AGENT_START", {"input": user_input, "model": self.llm.model_name})
        
        current_prompt = user_input
        steps = 0

        while steps < self.max_steps:
            # TODO: Generate LLM response
            # result = self.llm.generate(current_prompt, system_prompt=self.get_system_prompt())
            
            # TODO: Parse Thought/Action from result
            
            # TODO: If Action found -> Call tool -> Append Observation
            
            # TODO: If Final Answer found -> Break loop
            
            steps += 1
            
        logger.log_event("AGENT_END", {"steps": steps})
        return "Not implemented. Fill in the TODOs!"

    def _tool_attr(self, tool: Any, name: str, default: Any = None) -> Any:
        if isinstance(tool, dict):
            return tool.get(name, default)
        return getattr(tool, name, default)

    def _execute_tool(self, tool_name: str, args: str) -> str:
        """
        Helper method to execute tools by name.
        """
        for tool in self.tools:
            if self._tool_attr(tool, "name") == tool_name:
                handler = self._tool_attr(tool, "handler")
                input_model = self._tool_attr(tool, "input_model")
                if not callable(handler):
                    return f"Result of {tool_name}"
                try:
                    parsed_args: Any = args
                    if isinstance(args, str):
                        parsed_args = json.loads(args)
                    if input_model is not None and isinstance(parsed_args, dict):
                        parsed_args = input_model.model_validate(parsed_args)
                    result = handler(parsed_args)
                    if hasattr(result, "model_dump_json"):
                        return result.model_dump_json()
                    return str(result)
                except Exception as exc:
                    return f"Tool execution error for {tool_name}: {exc}"
        return f"Tool {tool_name} not found."
