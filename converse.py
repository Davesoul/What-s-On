from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai import Credentials
from langchain_ibm import ChatWatsonx

from ibm_watsonx_ai.foundation_models import ModelInference
from dotenv import load_dotenv
import os

load_dotenv()

api = os.getenv('WATSONX_APIKEY')
project_id = os.getenv('PROJECT_ID')

credentials = Credentials(
    url = "https://eu-de.ml.cloud.ibm.com",
    api_key = api
)


client = APIClient(credentials)

params = {
    "time_limit": 10000,
    "max_new_token": 100
}

model_id = "meta-llama/llama-3-1-70b-instruct"
space_id = None # optional
verify = False

# model = ModelInference(
#   model_id=model_id,
#   api_client=client,
#   project_id=project_id,
#   params=params,
#   verify=verify,
# )

model = ChatWatsonx(
    model_id="meta-llama/llama-3-1-70b-instruct",
    url="https://eu-de.ml.cloud.ibm.com",
    params=params,
    project_id=project_id,

)

translation_model = ChatWatsonx(
    model_id="ibm/granite-20b-multilingual",
    url="https://eu-de.ml.cloud.ibm.com",
    params=params,
    project_id=project_id,

)


messages = [
  {
    "role": "system",
    "content": "You are a helpful assistant."
  },
  {
    "role": "user",
    "content": [
      {
        "type": "text",
        "text": "How far is Paris from Bangalore?"
      }
    ]
  },
  {
    "role": "assistant",
    "content": "The distance between Paris, France, and Bangalore, India, is approximately 7,800 kilometers (4,850 miles)"
  }
]


def cache(messages, role, content):
    messages.append({
        "role": role,
        "content": [
            {
                "type": "text",
                "text": content
            }
        ]
    })



if __name__ == "__main__":
    while True:
        message = input("> ")
        if message:
            messages.append({
              "role": "user",
              "content": [
                {
                  "type": "text",
                  "text": message
                }
              ]
            })
        stream_response = model.chat_stream(messages=messages)

        full_response = ""

        for chunk in stream_response:
            if next(iter(chunk['choices'][0]['delta'])) == "content":
                content = chunk['choices'][0]['delta']['content']
                print(content, end='')
                full_response += content

        messages.append({
          "role": "assistant",
          "content": [
            {
              "type": "text",
              "text": full_response
            }
          ]
        })

        print(messages)


