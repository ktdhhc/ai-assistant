#!/usr/bin/python 3.10

import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_deepseek import ChatDeepSeek
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory, ConversationSummaryMemory, ConversationSummaryBufferMemory, ConversationTokenBufferMemory
from langchain.prompts import MessagesPlaceholder
from langchain.chains import ConversationChain
from langchain_community.utilities import WikipediaAPIWrapper

def get_chat_response(input, memory, api_key, role_prompt, creativity=0.5, chat_model='DeepSeek'):
    
    if role_prompt and not memory.chat_memory.messages:
        memory.chat_memory.add_ai_message(role_prompt) 

    if chat_model == 'DeepSeek':
        model = ChatDeepSeek(model='deepseek-chat',
                            api_key = api_key,
                            temperature = creativity)
    elif chat_model == 'Chat_GPT':
        model = ChatOpenAI(model="gpt-3.5-turbo", 
                            openai_api_key = api_key,
                            openai_api_base = "https://api.aigc369.com/v1",
                            temperature = creativity)

    chain = ConversationChain(llm=model, memory=memory)
    response = chain.invoke({'input': input})

    return response['response']

