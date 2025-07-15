#!/usr/bin/python 3.10

import streamlit as st
import pandas as pd
from apply import get_chat_response
from langchain.memory import ConversationBufferWindowMemory
import random
import importlib
import role as r
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
importlib.reload(r)  

# 读取默认角色
default_roles = r.default_roles
role_manager = r.RoleManager(default_roles)

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

    selected_role = st.selectbox('请选择角色：', ['Zuan', 'Lyra', 'Kiri', '自定义', '混乱模式🤯'])

    if selected_role == '自定义':
        custom_prompt = st.text_area('请输入AI角色设定：')
        custom_role = r.ChatRole(
            name="ai",
            prompt=custom_prompt,
            title="私人助手😊",
            start_msg="有什么可以帮到您？"
        )
        role_manager.add_role(custom_role)
        current_role = custom_role
    elif selected_role == '混乱模式🤯':
        current_role = role_manager.get_random_role()
    else:
        current_role = role_manager.get_role(selected_role)

    st.divider()
    

    # 保存会话
    if 'memory' not in st.session_state:
        # 初始化记忆
        st.session_state.memory = ConversationBufferWindowMemory(
            return_messages=True, 
            k=5,
            memory_key="history",  # 明确指定记忆键
            input_key="input"  # 明确指定输入键
        )
        # 初始化消息
        st.session_state.messages = [AIMessage(content='有什么可以帮到您？')]
        # 注入角色提示词
        if selected_role != '混乱模式🤯':  # 混乱模式不固定提示
            st.session_state.memory.chat_memory.add_message(SystemMessage(content=current_role.prompt))


    # 清空数据
    clear = st.button('清理缓存')
    # 定义对话框
    @st.dialog("确认操作")
    def confirm_action():
        st.write("确定要执行此操作吗？")
        if st.button("确认"):
            st.session_state.confirmed = True
            # 清空所有数据缓存
            st.cache_data.clear()
            # 清空所有资源缓存（如模型、数据库连接）
            st.cache_resource.clear()
            st.session_state.messages.clear()
            st.session_state.memory.clear()
            st.rerun()  # 刷新页面
    if clear:
        confirm_action()
    # 处理确认结果
    if st.session_state.get("confirmed"):
        st.success("数据已清空！")
        del st.session_state.confirmed

# 标题
st.title(current_role.title)
f'##### {current_role.start_msg}'
st.divider()

# 打印消息
for message in st.session_state.messages:
    # 确定消息角色
    if isinstance(message, HumanMessage):
        role = "human"
    elif isinstance(message, AIMessage):
        role = "ai"
    else:
        role = "ai"  # 默认值
    st.chat_message(role).write(message.content)

# 接收输入
input = st.chat_input()
if input:
    if not api_key:
        st.info('请输入api密钥')
        st.stop()

    # 保存和打印用户输入
    st.session_state.messages.append(HumanMessage(content=input))
    st.chat_message('human').write(input)

    # 重置记忆并注入新提示
    st.session_state.memory = ConversationBufferWindowMemory(
        return_messages=True, 
        k=10,
        memory_key="history",
        input_key="input"
    )
    st.session_state.memory.chat_memory.add_message(SystemMessage(content=current_role.prompt))

    # # === 混乱模式处理 ===
    # if selected_role == "混乱模式🤯":
    #     # 每次对话获取新随机角色
    #     current_role = role_manager.get_random_role()
    #     st.session_state.current_chaos_role = current_role  # 存储当前角色
        
    #     # 重置记忆并注入新提示
    #     st.session_state.memory = ConversationBufferWindowMemory(
    #         return_messages=True, 
    #         k=5,
    #         memory_key="history",
    #         input_key="input"
    #     )
    #     st.session_state.memory.chat_memory.add_message(SystemMessage(content=current_role.prompt))

    # elif custom_role:  # 自定义角色处理
    #     st.session_state.memory.chat_memory.add_message(SystemMessage(content=custom_role.prompt))


    # 调用模型
    with st.spinner('ai正在思考，请稍候...'):
        response = get_chat_response(input = input, 
                                     memory = st.session_state.memory, 
                                     api_key = api_key, 
                                     chat_model = model_name)
        
    # 保存和打印模型输出
    st.session_state.messages.append(AIMessage(content=response))
    st.chat_message('ai').write(response)

