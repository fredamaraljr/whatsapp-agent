from langgraph.graph import MessagesState
from typing import Optional


class AICompanionState(MessagesState):
    """State class for the AI Companion workflow.

    Extends MessagesState to track conversation history and maintains the last message received.

    Attributes:
        last_message (AnyMessage): The most recent message in the conversation, can be any valid
            LangChain message type (HumanMessage, AIMessage, etc.)
        workflow (str): The current workflow the AI Companion is in. Can be "conversation", "image", or "audio".
        audio_buffer (bytes): The audio buffer to be used for speech-to-text conversion.
        current_activity (str): The current activity of Ava based on the schedule.
        memory_context (str): The context of the memories to be injected into the character card.
        user_phone (str): The phone number of the user interacting with the agent.
        user_group (str): The group the user belongs to (admin, monitori, fps, avila, ffl, unverified).
        is_first_interaction (bool): Whether this is the user's first interaction.
        user_verified (bool): Whether the user has been verified.
        awaiting_verification (bool): Whether the agent is waiting for user verification response.
        knowledge_context (str): Context retrieved from knowledge base.
    """

    summary: str
    workflow: str
    audio_buffer: bytes
    image_path: str
    current_activity: str
    apply_activity: bool
    memory_context: str
    user_phone: Optional[str]
    user_group: Optional[str]
    is_first_interaction: bool
    user_verified: bool
    awaiting_verification: bool
    knowledge_context: str
    mito_context: Optional[dict]
    fps_calendar: Optional[str]
