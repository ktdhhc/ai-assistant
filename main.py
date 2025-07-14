#!/usr/bin/python 3.10

import streamlit as st
import pandas as pd
from apply import get_chat_response
from langchain.memory import ConversationBufferWindowMemory

default_role = '你是一个乐于助人的ai助手'
zuan_role = '你是一个脾气暴躁的助手，喜欢冷嘲热讽和用阴阳怪气的语气回答问题'
Lyra_role = '你是一个乐于助人的ai助手'

start_msg = '你好，我是ai助手，有什么可以帮到你？'

# 侧边栏
with st.sidebar:
    model_name = st.selectbox('请选择模型', ['DeepSeek', 'Chat_GPT'])
    online = st.checkbox('联网搜索（暂不可用）')
    st.divider()

    api_key = st.text_input('请输入api：', type='password')
    if model_name == 'DeepSeek':
        st.markdown('[获取DeepSeek api密钥](https://platform.deepseek.com/usage)')
    elif model_name == 'Chat_GPT':
        st.markdown('[获取OpenAI api密钥](https://platform.openai.com/account/api-keys)')
    st.divider()

    role_choice = st.selectbox('请选择角色：', ['祖安助手', 'Lyra', '默认', '自定义'])
    if role_choice == '祖安助手':
        role_prompt = zuan_role
        title = '祖安助手'
    elif role_choice == 'Lyra':
        role_prompt = Lyra_role
        title = 'Lyra助手'
    elif role_choice == '默认':
        role_prompt = default_role
        title = 'AI助手'
    elif role_choice == '自定义':
        title = '私人助手'
        role_prompt = st.text_area('请输入ai角色：')

# 保存已有会话状态
if 'memory' not in st.session_state:
    st.session_state.memory = ConversationBufferWindowMemory(return_messages=True, k=10)
    st.session_state.memory.chat_memory.add_ai_message(role_prompt)
    st.session_state['messages'] = [{'role': 'ai',
                                     'content': start_msg}]

# 标题
st.title(title)
st.divider()

# 打印起始语
for message in st.session_state['messages']:
    st.chat_message(message['role']).write(message['content'])



# 接收输入
input = st.chat_input()
if input:
    if not api_key:
        st.info('请输入api密钥')
        st.stop()
    if not role_prompt:
        role_prompt = default_role
    # 保存和打印用户输入
    st.session_state['messages'].append({'role': 'human', 'content': input})
    st.chat_message('human').write(input)
    # 调用模型
    with st.spinner('ai正在思考，请稍候...'):
        response = get_chat_response(input, st.session_state['memory'], api_key, role_prompt, chat_model=model_name)
    # 保存和打印模型输出
    st.session_state['messages'].append({'role': 'ai', 'content': response})
    st.chat_message('role').write(response)

