import os
from agency_swarm import Agent
from shared.agent_context import AgentContext, create_agent_context
from shared.agent_utils import select_instructions_file, create_model_settings, get_model_instance
from shared.system_hooks import create_message_filter_hook, create_memory_integration_hook, create_composite_hook
from tools import LS, Read, Grep, Glob, TodoWrite, Write, Edit, Bash
from .tools.architecture_loop import RunArchitectureLoop

current_dir = os.path.dirname(os.path.abspath(__file__))


def create_chief_architect_agent(model: str = "gpt-5", reasoning_effort: str = "high", agent_context: AgentContext | None = None) -> Agent:
    if agent_context is None:
        agent_context = create_agent_context()

    filter_hook = create_message_filter_hook()
    memory_hook = create_memory_integration_hook(agent_context)
    combined_hook = create_composite_hook([filter_hook, memory_hook])

    agent_context.store_memory(
        f"agent_created_{agent_context.session_id}",
        {
            "agent_type": "ChiefArchitectAgent",
            "model": model,
            "reasoning_effort": reasoning_effort,
            "session_id": agent_context.session_id,
        },
        ["agency", "chief_architect", "creation"],
    )

    return Agent(
        name="ChiefArchitectAgent",
        description="The strategic leader and architect. Reviews audit results and VectorStore knowledge to identify systemic improvements. Initiates autonomous improvement cycles through [SELF-DIRECTED TASK] entries, driving the agency's continuous evolution.",
        instructions=select_instructions_file(current_dir, model),
        model=get_model_instance(model),
        hooks=combined_hook,
        tools=[LS, Read, Grep, Glob, TodoWrite, Write, Edit, Bash, RunArchitectureLoop],
        tools_folder=os.path.join(current_dir, "tools"),
        model_settings=create_model_settings(model, reasoning_effort),
    )
