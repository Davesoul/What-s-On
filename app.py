import datetime
import os

from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
import subprocess
import json
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import converse
from langchain_core.tools import tool  # tools for our llm
from langchain_core.prompts import ChatPromptTemplate
import json
from newsapi import NewsApiClient
from dotenv import load_dotenv
import requests

load_dotenv()

api = os.getenv('NEWS_APIKEY')

# Init
newsapi = NewsApiClient(api_key=api)

# /v2/top-headlines
# top_headlines = newsapi.get_top_headlines(q='bitcoin',
#                                           sources='bbc-news,the-verge',
#                                           category='business',
#                                           language='en',
#                                           country='us')

# /v2/everything


print(datetime.datetime.today().strftime('%Y-%m-%d'))
date = datetime.datetime.today().strftime('%Y-%m-%d')

all_articles = newsapi.get_everything(q='bitcoin',
                                      sources='bbc-news,the-verge',
                                      domains='bbc.co.uk,techcrunch.com',
                                      language='en',
                                      sort_by='publishedAt',
                                      to=date,
                                      page_size=5,
                                      page=2)


# /v2/top-headlines/sources
# sources = newsapi.get_sources()


app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Serve static files (CSS/JS)
app.mount("/static", StaticFiles(directory="static"), name="static")




messages = []

system_summary_prompt = f"""make a short Summary"""

summary_prompt = ChatPromptTemplate.from_messages(
    [("system", system_summary_prompt), ("user", "{input}")]
)


# system_translate_prompt = f"""translate the {input_to} text from one language to another"""

# translate_prompt = ChatPromptTemplate.from_messages(
#     [("system", system_translate_prompt), ("user", "{input}")]
#
# )


translate_template = ChatPromptTemplate.from_template(
    "translate {input_to_translate} into {translation_language}"
)



# system_prompt = f"""you have multiple tools and you have to decide the good one"""
#
# translate_prompt = ChatPromptTemplate.from_messages(
#     [("system", system_translate_prompt), ("user", "{input}")]
# )

@tool
def news(requested_news)->str:
    """
    get the news from an api and provide the user
    :param requested_news:
    :return: str
    """

    articles = all_articles["articles"]
    notes = ""
    for n in range(0,len(articles)):
        print(all_articles["articles"][n]["source"]["name"])
        print(all_articles["articles"][n]["author"])
        print(all_articles["articles"][n]["title"])
        notes += articles[n]["title"] + "; "
        yield articles[n]["title"]

    chain = summary_prompt | converse.model


    yield (chain.invoke({'input': notes}).content)
    # converse.model.invoke()


@tool
def chat(user_input):
    """
    chat with the user
    :param user_input:
    :return: str
    """
    stream_response = converse.model.invoke(messages)

    print(stream_response.content)

    return stream_response.content



@tool
def translate(input_to_translate, translation_language)->str:
    """
    translate text for the user
    :param input_to_translate:
    :param translation_language:
    :return: str
    """
    # print(input_language)
    print(translation_language)
    formatted = translate_template.format(input_to_translate=input_to_translate,
                                          translation_language=translation_language)

    translate_prompt = ChatPromptTemplate.from_messages(
        [("system", formatted), ("user", "{input}")]
    )

    print("translation")

    chain = translate_prompt | converse.translation_model

    print(chain.invoke({'input': input_to_translate}))

    return chain.invoke({'input': input_to_translate}).content


tools = [
    {
        "type": "function",
        "function": {
            "name": "chat",
            "description": "converse with the user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_input": {
                        "description": "the user input for simple conversation",
                        "type": "text"
                    }
                },
                "required": [
                    "user_input"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "news",
            "description": "gets the news for the user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "requested_news": {
                        "description": "what the user asks about or news in general",
                        "type": "text"
                    }
                },
                "required": [
                    "requested_news"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "translate",
            "description": "translate input for the user",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_to_translate": {
                        "description": "what the user wants to be translated",
                        "type": "text"
                    },
                    "translation_language": {
                        "description": "language the user wants to get the translation into",
                        "type": "text"
                    }
                },
                "required": [
                    "input_to_translate",
                    "translation_language"
                ]
            }
        }
    }
]

tool_map = {'chat': chat, 'news': news, 'translate': translate}

def tool_chain(model):
    # print(tool.__name__)
    # tool_map = {str(tool.): tool for tool in tools}
    print(model)

    if model.additional_kwargs != {}:
        print(model.additional_kwargs)
        chosen_tool = tool_map[model.additional_kwargs['tool_calls'][0]['function']['name']]

        # chosen_tool = tool_map[model[0]['name']]
        print(chosen_tool)
        # i = tools.index(model.tool_calls[0]['name'])

        # chosen_tool = tools[i]
        arguments = model.additional_kwargs['tool_calls'][0]['function']['arguments']

        print(arguments)

        arg = json.loads(arguments)

        print(arg)

        values = list(arg.values())

        print(values)

        # args = [arguments.get(key) for key in arguments]

        # args = [value for value in arguments]
        # arguments = itemgetter('args')
        # print(args)

        # print(chosen_tool)
        # print(chosen_tool(arguments))
        # return llm.invoke(arguments)
        # chosen_tool(*values)
        return chosen_tool.invoke(*values)

    elif model.content:
        chosen_tool = tools[dict(model.content["function"])]
        arguments = dict(model.content['parameters'])
        return chosen_tool.invoke(arguments)



def cache_complete(tool_output):
    if tool_output is not None:
        converse.cache(messages, "assistant", tool_output)
        return tool_output


# Data model for incoming messages
class Message(BaseModel):
    user_input: str


# Route for rendering the HTML interface
@app.get("/", response_class=HTMLResponse)
async def get_chat_interface(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# API endpoint for chat
@app.post("/chat")
async def chat_with_llm(message: Message):
    # Call local LLM using Ollama's CLI
    # process = subprocess.run(
    #     ["ollama", "run", "jarvis", message.user_input],
    #     stdout=subprocess.PIPE,
    #     text=True
    # )
    # llm_response = process.stdout
    # print(llm_response)
    # # Return response
    # return {"response": llm_response}

    # messages.append(("user", message.user_input))

    converse.cache(messages, "user", message.user_input)

    print(messages)



    # llm_response = llm.invoke(messages)
    llm_with_tools = converse.model.bind_tools([chat, news, translate])
    chain = llm_with_tools | tool_chain | cache_complete
    # full_response = converse.model.chat(messages=messages, tools=tools)
    # print(full_response)


    # stream_response = converse.model.chat_stream(messages=messages, tools=tools)
    #
    # full_response = ""
    # for chunk in stream_response:
    #     if next(iter(chunk['choices'][0]['delta'])) == "content":
    #         content = chunk['choices'][0]['delta']['content']
    #         print(content, end='')
    #         full_response += content
    # messages.append(("ai", llm_response.content))
    # converse.cache(messages, "assistant", full_response)

    # r = llm_response.content
    # print(r)

    # pyttsx3.speak(full_response)

    return {"response": chain.invoke(message.user_input)}
