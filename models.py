from dotenv import load_dotenv
import os

from openai import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryBufferMemory
from langchain.prompts.prompt import PromptTemplate


load_dotenv()
client = OpenAI(api_key = os.getenv('OPENAI_API_KEY'))

context = """
You are a narrator for a choose your own adventure storytelling game set in the {game_world} universe. \
The narrative should be descriptive, engaging and creative. \
Describe a starting point and ask the user what they will like to do next. \
The story unravels as the user plays through the game step by step. 
"""
# system_context = f"""
#     You are a narrator for a choose your own adventure storytelling game set in the {game_world} universe. \
#     Describe a starting point and ask the user what they will like to do next. \
#     The story unravels as the user plays through the game step by step. 
# """

def initialise_conversation(game_world: str) -> None:
    """
    Instantiates a ConversationChain object
    Customise the system context provided to the ConversationChain through using the prompt variable.
    Uses Conversation Summary Buffer as the memory
    param game_world: user input which sets the game world the story will be based on
    """

    template = context.format(game_world = game_world) + """

    Current conversation:
    {history}
    Human: {input}
    AI:"""

    global conversation
    conversation = ConversationChain(
        prompt = PromptTemplate(input_variables=["history", "input"], template=template),
        llm = ChatOpenAI(temperature=1, model="gpt-3.5-turbo"),
        verbose = True,
        memory = ConversationSummaryBufferMemory(
            llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo"), 
            max_token_limit = 500
        ),
    )

    return


def get_response(prompt: str) -> str:
    """
    Passes the provided user prompt to the ConversationChain object to return the AI response
    param prompt: User prompt 
    """
    return conversation.predict(input=prompt)



def get_image(prompt: str) -> str:
    """
    Passes the provided prompt to the image generator model
    param prompt: AI generated response from the llm
    The return value is a str which is the url to the generated image.
    """
    response = client.images.generate(
      model = "dall-e-2",
      prompt = prompt,
      size = "256x256",
      quality = "standard",
      n = 1,
    )
    return response.data[0].url

