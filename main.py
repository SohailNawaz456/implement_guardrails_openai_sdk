# Import necessary libraries
import os
from dotenv import load_dotenv

# Import agent framework classes and types
from agents import (
    Agent,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    set_tracing_disabled,
    input_guardrail,
    RunContextWrapper,
    TResponseInputItem,
    GuardrailFunctionOutput,
    InputGuardrail,
)

# Import Pydantic for creating structured output models
from pydantic import BaseModel

# Import Chainlit for building interactive chat applications
import chainlit as cl

# Load environment variables from .env file
load_dotenv()

# Disable tracing if desired (e.g. for privacy or performance)
set_tracing_disabled(disabled=True)

# Retrieve the Gemini API key from environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Initialize the AsyncOpenAI client pointing to Google's Gemini endpoint
client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Create an OpenAI-compatible chat completions model for Gemini
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client,
)

# ---------------------------------------------------------------
# Define a Pydantic output schema for the guardrail agent's output
# ---------------------------------------------------------------
class Output_Python(BaseModel):
    is_python_related: bool      # Whether the question relates to Python
    reasoning: str               # Explanation or reasoning for the result

# ---------------------------------------------------------------------
# Create an agent to check if a user question is Python-related or not
# ---------------------------------------------------------------------
input_guardrails_agent = Agent(
    name="input Guardrails Checker",
    instructions=(
        "Check if the user's question is related to Python programming. "
        "If it is, return true. If it is not, return false."
    ),
    model=model,
    output_type=Output_Python
)

# -------------------------------------------------------
# Define an async function to execute the input guardrail
# -------------------------------------------------------
async def input_guardrail_func(
    ctx: RunContextWrapper,
    agent: Agent,
    input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    """
    Run the input guardrail agent to determine if the user's question
    is related to Python. If not, set the tripwire to True.
    """
    # Run the guardrail agent and capture the result
    result = await Runner.run(
        input_guardrails_agent,
        input
    )

    # Return GuardrailFunctionOutput indicating whether the tripwire was triggered
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=not result.final_output.is_python_related
    )

# -------------------------------------------------------------------------
# Define the main Python expert agent that only answers Python-related questions
# -------------------------------------------------------------------------
main_agent = Agent(
    name="Python Expert Agent",
    instructions=(
        "You are a Python expert agent. "
        "You respond only to Python-related questions."
    ),
    model=model
)

# ---------------------------------------------------------
# Chainlit callback for when a chat session is started
# ---------------------------------------------------------
@cl.on_chat_start
async def on_chat_start():
    # Send welcome message to the user
    await cl.Message(content="Hi, I am ready to assist you!").send()

# ---------------------------------------------------------
# Chainlit callback for handling incoming messages
# ---------------------------------------------------------
@cl.on_message
async def on_message(message: cl.Message):
    try:
        # First, check if the user’s message is Python-related using the guardrail
        guardrail_result = await input_guardrail_func(
            None,  # ctx is optional and not used here
            main_agent,
            message.content
        )

        # If the guardrail was triggered, block non-Python questions
        if guardrail_result.tripwire_triggered:
            await cl.Message(content="Sorry, I can only answer Python-related questions.").send()
            return

        # Otherwise, run the main Python expert agent
        result = await Runner.run(
            main_agent,
            input=message.content
        )

        # Send the agent’s final output as a message
        await cl.Message(content=result.final_output).send()

    except Exception as e:
        # Send error details if something goes wrong
        await cl.Message(content=f"Error: {e}").send()
