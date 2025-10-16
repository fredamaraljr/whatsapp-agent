from langgraph.graph import END
from typing_extensions import Literal

from ai_companion.graph.state import AICompanionState
from ai_companion.settings import settings


def should_summarize_conversation(
    state: AICompanionState,
) -> Literal["summarize_conversation_node", "__end__"]:
    messages = state["messages"]

    if len(messages) > settings.TOTAL_MESSAGES_SUMMARY_TRIGGER:
        return "summarize_conversation_node"

    return END


def select_workflow(
    state: AICompanionState,
) -> Literal["conversation_node", "image_node", "audio_node"]:
    workflow = state["workflow"]

    if workflow == "image":
        return "image_node"

    elif workflow == "audio":
        return "audio_node"

    else:
        return "conversation_node"


def should_verify_user(
    state: AICompanionState,
) -> Literal["group_verification_node", "admin_command_node"]:
    """Check if user needs verification or if admin command should be processed."""
    user_verified = state.get("user_verified", False)
    awaiting_verification = state.get("awaiting_verification", False)
    is_first_interaction = state.get("is_first_interaction", False)
    user_group = state.get("user_group", "unverified")
    
    # If user is admin and message starts with /, go to admin command node
    if user_group == "admin":
        last_message = state["messages"][-1].content if state["messages"] else ""
        if last_message.strip().startswith("/"):
            return "admin_command_node"
    
    # If user is not verified or awaiting verification, go to verification node
    if not user_verified or awaiting_verification or (is_first_interaction and user_group == "unverified"):
        return "group_verification_node"
    
    # Otherwise, continue to normal flow
    return "memory_extraction_node"


def after_verification(
    state: AICompanionState,
) -> Literal["memory_extraction_node", "__end__"]:
    """After verification, either continue to normal flow or end if just sent verification question."""
    awaiting_verification = state.get("awaiting_verification", False)
    
    # If we just sent verification question, end here (wait for user response)
    if awaiting_verification and state.get("is_first_interaction", False):
        return END
    
    # Otherwise continue to normal flow
    return "memory_extraction_node"


def after_admin_command(
    state: AICompanionState,
) -> Literal["memory_extraction_node", "__end__"]:
    """After admin command, check if we should continue or end."""
    # If the last message is from AI (command response), end here
    if state["messages"] and hasattr(state["messages"][-1], "type"):
        # Check if command was processed
        last_user_message = None
        for msg in reversed(state["messages"]):
            if msg.type == "human":
                last_user_message = msg.content
                break
        
        if last_user_message and last_user_message.strip().startswith("/"):
            return END
    
    # Otherwise continue to normal conversation flow
    return "memory_extraction_node"
