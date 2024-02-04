from models import get_response, get_image, initialise_conversation

import streamlit as st

from langchain.schema import (
    HumanMessage,
    AIMessage
)

# Assign True or False - generates or does not generate images by the AI respectively.
GENERATE_IMAGE = True

def main() -> None:

    st.header("AI Storyteller - Choose Your Own Adventure Game :game_die:")

    game_world = st.sidebar.text_input(f"Enter game world:", max_chars=20)

    start_button = st.sidebar.button("Start game")

    # Restart of game by user. Deletes conversation history.
    if st.sidebar.button("Restart"):
        for key in st.session_state.keys():
            del st.session_state[key]

    # Display chat messages from history
    messages = st.session_state.get('messages', [])
    # for message in messages:
    #     st.chat_message(message["role"]).markdown(message["content"])
    for i, msg in enumerate(messages):
        if i % 2 != 0:
            st.chat_message("user").write(msg.content)
        else:
            st.chat_message("assistant").write(msg.content)

    # Starts game. Initialises session_state and conversation.
    if game_world and start_button:

        # Only execute on the first run
        if "messages" not in st.session_state:

            initialise_conversation(game_world)

            st.session_state.messages = []
            
            # Get AI to start the story
            generate_response("start the game", st.session_state.messages)

    # Next conversation - user input and assistant response
    if prompt := st.chat_input("Your message: "):

        # Display user message and append to session state messages
        st.chat_message("user").write(prompt)
        st.session_state.messages.append(
            HumanMessage(content=prompt)
        )

        # Get AI response based on the user input
        generate_response(prompt, st.session_state.messages)

    return


def generate_response(prompt: str, messages: list) -> None:
    """
    Generate llm response from messages and then use the response to generate DALL-E image.
    Display the AI generated response and image in the conversation window.
    """

    with st.chat_message("assistant"):

        with st.spinner("AI is thinking ..."):
            response = get_response(prompt)

        messages.append(
            AIMessage(content=response)
        )

        st.write(response)

        if GENERATE_IMAGE:
            generate_image(response)

    return

def generate_image(prompt: str) -> None:
    
    # 1,000 max characters for Dall E 2 prompt
    if len(prompt) > 1000:
        image_prompt = prompt[:1000]
    else:
        image_prompt = prompt

    with st.spinner("Generating image ..."):
        image_url = get_image(image_prompt)

    st.image(image_url)

    return


if __name__ == "__main__":
    main()

