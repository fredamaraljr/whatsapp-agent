from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel, Field

from ai_companion.core.prompts import (
    CHARACTER_CARD_PROMPT, 
    ROUTER_PROMPT,
    ADMIN_CHARACTER_PROMPT,
    MONITORI_CHARACTER_PROMPT,
    FPS_CHARACTER_PROMPT,
    AVILA_CHARACTER_PROMPT,
    FFL_CHARACTER_PROMPT,
    UNVERIFIED_USER_PROMPT,
)
from ai_companion.graph.utils.helpers import AsteriskRemovalParser, get_chat_model


class RouterResponse(BaseModel):
    response_type: str = Field(
        description="The response type to give to the user. It must be one of: 'conversation', 'image' or 'audio'"
    )


def get_router_chain():
    model = get_chat_model(temperature=0.3).with_structured_output(RouterResponse)

    prompt = ChatPromptTemplate.from_messages(
        [("system", ROUTER_PROMPT), MessagesPlaceholder(variable_name="messages")]
    )

    return prompt | model


def get_prompt_for_group(user_group: str) -> str:
    """Get the appropriate character prompt based on user group."""
    group_prompts = {
        "admin": ADMIN_CHARACTER_PROMPT,
        "monitori": MONITORI_CHARACTER_PROMPT,
        "fps": FPS_CHARACTER_PROMPT,
        "avila": AVILA_CHARACTER_PROMPT,
        "ffl": FFL_CHARACTER_PROMPT,
        "unverified": UNVERIFIED_USER_PROMPT,
    }
    return group_prompts.get(user_group, CHARACTER_CARD_PROMPT)


def get_character_response_chain(
    summary: str = "", 
    knowledge_context: str = "", 
    memory_context: str = "", 
    current_activity: str = "",
    user_group: str = "ffl",  # Default to FFL (original behavior)
    fps_calendar: str = "",
    admin_commands_obj = None
):
    model = get_chat_model()
    
    # Get the appropriate prompt for the user's group
    base_prompt = get_prompt_for_group(user_group)
    
    # Check if admin has custom prompt for this group
    if admin_commands_obj:
        custom_prompt = admin_commands_obj.get_custom_prompt(user_group)
        if custom_prompt:
            base_prompt = custom_prompt
    
    # Format the prompt with context
    system_message = base_prompt.format(
        memory_context=memory_context,
        current_activity=current_activity,
        knowledge_context=knowledge_context,
        fps_calendar=fps_calendar if user_group == "fps" else "",
    )

    if summary:
        system_message += f"\n\nSummary of conversation earlier between Ava and the user: {summary}"

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_message),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    return prompt | model | AsteriskRemovalParser()
