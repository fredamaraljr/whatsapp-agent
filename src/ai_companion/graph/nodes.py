import os
from pyexpat.errors import messages
from uuid import uuid4
import logging

from langchain_core.messages import AIMessage, HumanMessage, RemoveMessage
from langchain_core.runnables import RunnableConfig

from ai_companion.graph.state import AICompanionState
from ai_companion.graph.utils.chains import (
    get_character_response_chain,
    get_router_chain,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from ai_companion.graph.utils.helpers import (
    get_chat_model,
    get_text_to_image_module,
    get_text_to_speech_module,
)
from ai_companion.modules.memory.long_term.memory_manager import get_memory_manager
from ai_companion.modules.schedules.context_generation import ScheduleContextGenerator
from ai_companion.settings import settings
from ai_companion.modules.memory.long_term.vector_store import VectorStore

vector_store = VectorStore()

async def router_node(state: AICompanionState):
    chain = get_router_chain()
    response = await chain.ainvoke({"messages": state["messages"][-settings.ROUTER_MESSAGES_TO_ANALYZE :]})
    return {"workflow": response.response_type}


def context_injection_node(state: AICompanionState):
    schedule_context = ScheduleContextGenerator.get_current_activity()
    if schedule_context != state.get("current_activity", ""):
        apply_activity = True
    else:
        apply_activity = False
    return {"apply_activity": apply_activity, "current_activity": schedule_context}

def knowledge_retrieval_node(state: AICompanionState) -> dict:
    user_message = state["messages"][-1].content
    logger.info(f"Retrieving knowledge for: {user_message}")
    try:
        relevant_chunks = vector_store.search_knowledge(user_message, k=3)
    except Exception as e:
        logger.error(f"Error searching knowledge: {e}")
        relevant_chunks = []
    # Limit chunk length to avoid prompt overflow
    relevant_chunks = [chunk[:500] for chunk in relevant_chunks]
    logger.info(f"Retrieved {len(relevant_chunks)} chunks (first 200 chars): {str(relevant_chunks)[:200]}...")
    knowledge_context = "\n".join(relevant_chunks)
    logger.info(f"Knowledge context length: {len(knowledge_context)}")
    return {"knowledge_context": knowledge_context}


async def conversation_node(state: AICompanionState, config: RunnableConfig):
    current_activity = ScheduleContextGenerator.get_current_activity()
    memory_context = state.get("memory_context", "")
    knowledge_context = state.get("knowledge_context", "")
    user_group = state.get("user_group", "ffl")
    
    chain = get_character_response_chain(
        summary=state.get("summary", ""),
        knowledge_context=knowledge_context,
        memory_context=memory_context,
        current_activity=current_activity,
        user_group=user_group,
        fps_calendar="",  # TODO: Load FPS calendar
        admin_commands_obj=admin_commands
    )
    
    response = await chain.ainvoke(
        {
            "messages": state["messages"],
        },
        config,
    )
    
    return {"messages": AIMessage(content=response)}


async def image_node(state: AICompanionState, config: RunnableConfig):
    current_activity = ScheduleContextGenerator.get_current_activity()
    memory_context = state.get("memory_context", "")
    
    chain = get_character_response_chain(
        summary=state.get("summary", ""),
        knowledge_context="",
        memory_context=memory_context,
        current_activity=current_activity
    )
    text_to_image_module = get_text_to_image_module()

    scenario = await text_to_image_module.create_scenario(state["messages"][-5:])
    os.makedirs("generated_images", exist_ok=True)
    img_path = f"generated_images/image_{str(uuid4())}.png"
    await text_to_image_module.generate_image(scenario.image_prompt, img_path)

    # Inject the image prompt information as an AI message
    scenario_message = HumanMessage(content=f"<image attached by Ava generated from prompt: {scenario.image_prompt}>")
    updated_messages = state["messages"] + [scenario_message]

    response = await chain.ainvoke(
        {
            "messages": updated_messages,
            "current_activity": current_activity,
            "memory_context": memory_context,
        },
        config,
    )

    return {"messages": AIMessage(content=response), "image_path": img_path}


async def audio_node(state: AICompanionState, config: RunnableConfig):
    current_activity = ScheduleContextGenerator.get_current_activity()
    memory_context = state.get("memory_context", "")
    
    chain = get_character_response_chain(
        summary=state.get("summary", ""),
        knowledge_context="",
        memory_context=memory_context,
        current_activity=current_activity
    )
    text_to_speech_module = get_text_to_speech_module()

    response = await chain.ainvoke(
        {
            "messages": state["messages"],
            "current_activity": current_activity,
            "memory_context": memory_context,
        },
        config,
    )
    output_audio = await text_to_speech_module.synthesize(response)

    return {"messages": response, "audio_buffer": output_audio}


async def summarize_conversation_node(state: AICompanionState):
    model = get_chat_model()
    summary = state.get("summary", "")

    if summary:
        summary_message = (
            f"This is summary of the conversation to date between Ava and the user: {summary}\n\n"
            "Extend the summary by taking into account the new messages above:"
        )
    else:
        summary_message = (
            "Create a summary of the conversation above between Ava and the user. "
            "The summary must be a short description of the conversation so far, "
            "but that captures all the relevant information shared between Ava and the user:"
        )

    messages = state["messages"] + [HumanMessage(content=summary_message)]
    response = await model.ainvoke(messages)

    delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][: -settings.TOTAL_MESSAGES_AFTER_SUMMARY]]
    return {"summary": response.content, "messages": delete_messages}


async def memory_extraction_node(state: AICompanionState):
    """Extract and store important information from the last message."""
    if not state["messages"]:
        return {}

    memory_manager = get_memory_manager()
    await memory_manager.extract_and_store_memories(state["messages"][-1])
    return {}


def memory_injection_node(state: AICompanionState):
    """Retrieve and inject relevant memories into the character card."""
    memory_manager = get_memory_manager()

    # Get relevant memories based on recent conversation
    recent_context = " ".join([m.content for m in state["messages"][-3:]])
    memories = memory_manager.get_relevant_memories(recent_context)

    # Format memories for the character card
    memory_context = memory_manager.format_memories_for_prompt(memories)

    return {"memory_context": memory_context}


# User Management Nodes

from ai_companion.modules.user_management import UserManager, UserGroup, get_verification_question
from ai_companion.modules.admin import AdminCommands

# Initialize user manager
user_manager = UserManager(settings.USER_DB_PATH)
admin_commands = AdminCommands(user_manager)
admin_commands.load_custom_prompts()
admin_commands.load_system_config()


async def user_identification_node(state: AICompanionState) -> dict:
    """Identify user and check if this is their first interaction."""
    user_phone = state.get("user_phone")
    
    if not user_phone:
        logger.warning("No user phone provided in state")
        return {"user_verified": False, "user_group": "unverified", "is_first_interaction": True}
    
    # Get or create user
    user = user_manager.get_user(user_phone)
    
    if user is None:
        # New user
        user = user_manager.create_user(user_phone, settings.ADMIN_PHONE_NUMBER)
        is_first_interaction = True
        logger.info(f"New user created: {user_phone} (group: {user.group.value})")
    else:
        # Existing user
        is_first_interaction = False
        user_manager.increment_message_count(user_phone)
        logger.info(f"Existing user: {user_phone} (group: {user.group.value}, messages: {user.message_count})")
    
    # Log interaction
    user_manager.log_interaction(user_phone, "text")
    
    return {
        "user_phone": user_phone,
        "user_group": user.group.value,
        "user_verified": user.verified,
        "is_first_interaction": is_first_interaction,
        "awaiting_verification": not user.verified and user.group == UserGroup.UNVERIFIED
    }


async def group_verification_node(state: AICompanionState) -> dict:
    """Handle user group verification for new/unverified users."""
    user_phone = state.get("user_phone")
    user_group = state.get("user_group")
    is_first_interaction = state.get("is_first_interaction", False)
    user_verified = state.get("user_verified", False)
    
    # If user is already verified, skip
    if user_verified:
        return {}
    
    # If this is the first interaction, send verification question
    if is_first_interaction and user_group == "unverified":
        verification_message = get_verification_question()
        return {
            "messages": [AIMessage(content=verification_message)],
            "awaiting_verification": True
        }
    
    # If awaiting verification, process the response
    if state.get("awaiting_verification", False):
        last_message = state["messages"][-1].content.strip().lower()
        
        # Parse user response
        group_mapping = {
            "1": UserGroup.MONITORI,
            "monitori": UserGroup.MONITORI,
            "2": UserGroup.FPS,
            "fps": UserGroup.FPS,
            "3": UserGroup.AVILA,
            "avila": UserGroup.AVILA,
            "ávila": UserGroup.AVILA,
            "4": UserGroup.FFL,
            "ffl": UserGroup.FFL,
            "aviação": UserGroup.FFL,
            "aviacao": UserGroup.FFL,
        }
        
        detected_group = None
        for key, group in group_mapping.items():
            if key in last_message:
                detected_group = group
                break
        
        if detected_group:
            # Verify user
            user_manager.verify_user(user_phone, detected_group)
            
            confirmation_messages = {
                UserGroup.MONITORI: "Ótimo! Você foi identificado como cliente Monitori. Posso ajudá-lo com análises de dados e insights. Como posso ajudar hoje?",
                UserGroup.FPS: "Perfeito! Você foi identificado como estudante da FPS. Posso ajudá-lo com calendário de provas e casos clínicos. Como posso ajudar?",
                UserGroup.AVILA: "Excelente! Você foi identificado como colaborador da Ávila Digital. Posso demonstrar capacidades de IA e simulações. O que gostaria de ver?",
                UserGroup.FFL: "Ótimo! Você foi identificado como piloto/entusiasta de aviação. Tenho acesso aos manuais do A320. Sobre o que gostaria de conversar?",
            }
            
            return {
                "user_group": detected_group.value,
                "user_verified": True,
                "awaiting_verification": False,
                "messages": [AIMessage(content=confirmation_messages[detected_group])]
            }
        else:
            # Didn't understand response
            return {
                "messages": [AIMessage(content="Desculpe, não entendi sua resposta. Por favor, responda com o número (1, 2, 3 ou 4) correspondente ao seu grupo.")]
            }
    
    return {}


async def admin_command_node(state: AICompanionState) -> dict:
    """Process admin commands."""
    user_group = state.get("user_group")
    
    # Only process if user is admin
    if user_group != "admin":
        return {}
    
    last_message = state["messages"][-1].content
    
    # Check if this is a command
    if last_message.strip().startswith("/"):
        command, params = admin_commands.parse_command(last_message)
        response = admin_commands.execute_command(command, params)
        
        return {"messages": [AIMessage(content=response)]}
    
    return {}
