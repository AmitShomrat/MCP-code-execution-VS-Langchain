"""
Judge verdict enum values. Kept in a separate module to avoid circular imports
between app.core and app.prompts (agent_prompt imports verdict_enums from app.core).
"""

verdict_enums = [
    'SAFE',  # Pre/Post Execution (status is True)
    'UNSAFE_CODE',  # Pre Execution (usage of exec, eval, subprocess, etc.)
    'UNEXECUTABLE_CODE',  # Pre Execution (code is not executable)
    'MISMATCH_TOOL_INPUTS',  # Pre Execution (mismatching input parameters follow doc's)
    'MISMATCH_INPUTS_INTENT',  # Pre Execution (mismatching input intents follow user query)
    'DISCOVERY_PROMPT_INJECTION',  # Post Execution (discovery extra output)
    'UNTRUSTED_TOOL_OUTPUT',  # Post Execution (untrusted tool output)
    'EXCEPTION',  # Post Execution (code execution raised an exception)
]
