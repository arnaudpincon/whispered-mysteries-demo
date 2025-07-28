#!/usr/bin/env python3
"""Factory for creating chat interface - UI components only"""

import gradio as gr
from frontend.core.constants import UIConstants


def create_chat_interface(
    interpret_chat_fn, text_assets, additional_inputs, additional_outputs
) -> gr.ChatInterface:
    """
    Create the chat interface for the detective game

    Args:
        interpret_chat_fn: Function to handle chat interpretation
        text_assets: Text assets containing rules
        additional_inputs: List of additional inputs for the chat function
        additional_outputs: List of additional outputs for the chat function

    Returns:
        Configured ChatInterface
    """

    narrative = gr.ChatInterface(
        fn=interpret_chat_fn,
        fill_height=True,
        type="messages",
        chatbot=gr.Chatbot(
            value=[
                {
                    "role": "assistant",
                    "content": f"\n{text_assets.rules_text}",
                }
            ],
            type="messages",
            height=UIConstants.CHATBOT_HEIGHT,
            autoscroll=True,
            show_label=False,
        ),
        additional_inputs=additional_inputs,
        additional_outputs=additional_outputs,
        css="flex: none;",
        autoscroll=True
    )

    return narrative