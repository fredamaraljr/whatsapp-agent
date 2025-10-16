from functools import lru_cache

from langgraph.graph import END, START, StateGraph

from ai_companion.graph.edges import (
    select_workflow,
    should_summarize_conversation,
    should_verify_user,
    after_verification,
    after_admin_command,
)
from ai_companion.graph.nodes import (
    audio_node,
    context_injection_node,
    conversation_node,
    image_node,
    knowledge_retrieval_node,
    memory_extraction_node,
    memory_injection_node,
    router_node,
    summarize_conversation_node,
    user_identification_node,
    group_verification_node,
    admin_command_node,
)
from ai_companion.graph.state import AICompanionState


@lru_cache(maxsize=1)
def create_workflow_graph():
    graph_builder = StateGraph(AICompanionState)

    # Add all nodes
    graph_builder.add_node("user_identification_node", user_identification_node)
    graph_builder.add_node("group_verification_node", group_verification_node)
    graph_builder.add_node("admin_command_node", admin_command_node)
    graph_builder.add_node("memory_extraction_node", memory_extraction_node)
    graph_builder.add_node("router_node", router_node)
    graph_builder.add_node("context_injection_node", context_injection_node)
    graph_builder.add_node("memory_injection_node", memory_injection_node)
    graph_builder.add_node("conversation_node", conversation_node)
    graph_builder.add_node("image_node", image_node)
    graph_builder.add_node("audio_node", audio_node)
    graph_builder.add_node("summarize_conversation_node", summarize_conversation_node)
    graph_builder.add_node("knowledge_retrieval_node", knowledge_retrieval_node)
    graph_builder.add_edge("memory_injection_node", "knowledge_retrieval_node")
    graph_builder.add_edge("knowledge_retrieval_node", "conversation_node")

    # Define the flow
    # First identify user
    graph_builder.add_edge(START, "user_identification_node")
    
    # Check if user needs verification or admin command processing
    graph_builder.add_conditional_edges(
        "user_identification_node",
        should_verify_user,
        {
            "group_verification_node": "group_verification_node",
            "admin_command_node": "admin_command_node",
            "memory_extraction_node": "memory_extraction_node",
        }
    )
    
    # After verification, either continue or end
    graph_builder.add_conditional_edges(
        "group_verification_node",
        after_verification,
        {
            "memory_extraction_node": "memory_extraction_node",
            "__end__": END,
        }
    )
    
    # After admin command, either continue or end
    graph_builder.add_conditional_edges(
        "admin_command_node",
        after_admin_command,
        {
            "memory_extraction_node": "memory_extraction_node",
            "__end__": END,
        }
    )

    # Then determine response type
    graph_builder.add_edge("memory_extraction_node", "router_node")

    # Then inject both context and memories
    graph_builder.add_edge("router_node", "context_injection_node")
    graph_builder.add_edge("context_injection_node", "memory_injection_node")

    # Then proceed to appropriate response node
    graph_builder.add_conditional_edges("memory_injection_node", select_workflow)

    # Check for summarization after any response
    graph_builder.add_conditional_edges("conversation_node", should_summarize_conversation)
    graph_builder.add_conditional_edges("image_node", should_summarize_conversation)
    graph_builder.add_conditional_edges("audio_node", should_summarize_conversation)
    graph_builder.add_edge("summarize_conversation_node", END)

    return graph_builder


# Compiled without a checkpointer. Used for LangGraph Studio
graph = create_workflow_graph().compile()
