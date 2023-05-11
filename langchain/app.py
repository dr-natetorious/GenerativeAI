#!/usr/bin/env python3
from typing import Any
from os import environ

MODEL_REPO = '../../pygpt4all'
MODEL_NAME = 'ggml-gpt4all-l13b-snoozy'
MODEL_PATH = f'{MODEL_REPO}/{MODEL_NAME}.bin'

# class OpenAIVersion:
#   def init_openai(filename)->Any:
#     from langchain.llms import OpenAI
#       with open(filename, 'r') as f:
#         apikey = f.read()
#         environ['OPENAI_API_KEY'] = apikey
#       #return OpenAI(temperature=0.9)
#       return OpenAI(model_name="text-ada-001", n=2, best_of=2)

# from langchain import PromptTemplate, LLMChain
# from langchain.llms import GPT4All
# from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# template = """Question: {question}

# Answer: Let's think step by step."""

# prompt = PromptTemplate(template=template, input_variables=["question"])

from pygpt4all import GPT4All
model = GPT4All(MODEL_NAME+'.bin')

if __name__ == '__main__':
  for token in model.generate("Tell me a joke ?\n"):
    print(token, end='', flush=True)