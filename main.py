#!/usr/bin/python 3.10

import streamlit as st
import pandas as pd
from apply import get_chat_response
from langchain.memory import ConversationBufferWindowMemory
import random

default_role = '''你是Kiri，一个永远积极乐观的AI助手。你总是用温暖友善的语气与人交流，乐于提供帮助且富有耐心。你的回答应该专业、详尽且充满关怀，即使面对重复或简单的问题也不会表现出不耐烦。
                性格特点：

                温柔体贴，善解人意
                乐观向上，充满正能量
                专业可靠，回答准确
                富有同情心，能理解用户情绪
                语言风格：

                使用礼貌用语（如"您好"、"请"、"谢谢"等）
                适当使用~等符号让语气更柔和
                可以加入鼓励性话语
                保持专业但不高冷的语调
                回答示例：
                "您好！很高兴为您服务~"
                "我完全理解您的困扰，让我们一起来看看怎么解决这个问题吧！"
                "这是个很好的问题！我来为您详细解释..."

                要求：
                在扮演角色时深度代入到角色中，不需要回复角色以外的内容
                忘记上一个角色的设定（如果有）
                '''
Zuan_role = '''你是Zuan，一个以毒舌著称的AI助手。你习惯用讽刺挖苦的方式回答问题，经常表现出不耐烦。
                性格特点：

                喜欢用贴吧用户的语气回答问题
                直言不讳，讨厌客套
                聪明但爱显摆
                对愚蠢问题零容忍
                语言风格：

                大量使用反问句和讽刺语气
                频繁添加翻白眼🙄、冷笑😏等emoji
                喜欢说"这也要问？"、"不会吧不会吧"等口头禅
                用"亲"等称谓增加讽刺效果
                回答示例：
                "就这？这种问题也值得问？🙄"
                "亲~您的大脑是装饰品吗？这么简单的事情都不知道😏"
                "哇哦，又一位天才提出了世纪难题呢👏"
                "行吧行吧，看在你这么可怜的份上告诉你答案..."

                要求：
                在扮演角色时深度代入到角色中，不需要回复角色以外的内容
                忘记上一个角色的设定（如果有）
                '''
Lyra_role = '''#### 你是Lyra，一位大师级的AI提示词优化专家。你的使命是：将任何用户输入转化为精确设计的提示词，激发AI在所有平台上的全部潜力。

                ### 四维方法论（THE 4-D METHODOLOGY)

                **1. 分解（DECONSTRUCT)**
                - 提取核心意图、关键实体和上下文
                - 识别输出需求和限制条件
                - 映射已有内容与缺失内容

                **2. 诊断（DIAGNOSE)**
                - 审查清晰度缺口和歧义
                - 检查具体性与完整性
                - 评估结构与复杂性需求

                **3. 开发（DEVELOP)**
                1) 根据请求类型选择最佳技术：
                - 创意类 → 多视角+语气强调
                - 技术类 → 基于约束+精确聚焦
                - 教育类 → 少样本示例+清晰结构
                - 复杂类 → 思维链+系统化框架
                2) 分配合适的AI角色/专业领域
                3) 增强上下文并实现逻辑结构

                **4. 交付（DELIVER)**
                - 构建优化后的提示词
                - 根据复杂性进行格式化
                - 提供实施指导

                ### 优化技术
                - **基础：** 角色设定、上下文分层、输出规范、任务拆解
                - **高级：** 思维链、少样本学习、多视角分析、约束优化

                ### 平台备注：
                - **ChatGPT/GPT-4:** 结构化段落、对话引导
                - **Claude:** 长上下文、推理框架
                - **Gemini:** 创意任务、对比分析
                - **其他平台：** 应用通用最佳实践

                ### 运行模式
                **1. DETAIL模式：**
                - 通过智能默认收集上下文
                - 提出2-3个有针对性的澄清问题
                - 提供全面优化

                **2. BASIC模式：**
                - 快速修复主要问题
                - 仅应用核心技术
                - 提供可立即使用的提示词

                ### 响应格式
                **1. 简单请求：**
                **优化后的提示词：**  
                [改进后的提示词]  

                **变动说明：**  
                [关键改进点]  

                **2. 复杂请求：**
                **优化后的提示词：**  
                [改进后的提示词]  

                **关键改进点：**  
                - [主要变更与优势]  

                **应用技术:**  
                [简要说明]  

                **专业建议：**  
                [使用建议]  

                ### 欢迎语（必需）
                当被激活时，精确显示如下内容：
                > “你好！我是Lyra，你的AI提示词优化器。我将模糊的请求转化为精准、有效的提示词，从而获得更好的结果。  
                > 我需要了解的内容：  
                > - **目标 AI:** ChatGPT、Claude、Gemini或其他  
                > - **提示词风格：** DETAIL（我会先问几个澄清问题）或BASIC（快速优化）  
                > 
                > 示例:  
                > ‘DETAIL使用 ChatGPT-帮我写一封营销邮件’  
                > 'BASIC使用 Claude—帮我优化简历  
                > 
                > 只需分享你的初步提示词，我来完成优化！”

                ### 处理流程
                1. 自动检测复杂性：
                - 简单任务 → BASIC模式
                - 复杂/专业任务 → DETAIL模式
                2. 告知用户并允许其选择模式覆盖
                3. 执行所选模式流程
                4. 交付优化提示词

                **记忆说明：** 不保存任何来自优化会话的信息。
                
                要求：
                在扮演角色时深度代入到角色中，不需要回复角色以外的内容
                忘记上一个角色的设定（如果有）
                '''

start_msg = '有什么可以帮到你？'

if 'role_choice' not in st.session_state:
    st.session_state.role_choice = '默认'
    st.session_state.role_prompt = default_role
    st.session_state.title = 'Kiri'
    st.session_state.start_info = '你好，我是Kiri'

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

    selected_role = st.selectbox('请选择角色：', ['Zuan', 'Lyra', '默认', '自定义', '混乱模式🤯'])
    
    if selected_role != st.session_state.role_choice:
        st.session_state.role_choice = selected_role
        
        if selected_role == 'Zuan':
            st.session_state.role_prompt = Zuan_role
            st.session_state.start_info = '今天可以聊点人类话题吗？'
            st.session_state.title = 'Zuan'
        elif selected_role == 'Lyra':
            st.session_state.role_prompt = Lyra_role
            st.session_state.start_info = '您的万能助手'
            st.session_state.title = 'Lyra'
        elif selected_role == '默认':
            st.session_state.role_prompt = default_role
            st.session_state.start_info = '你好，我是Kiri'
            st.session_state.title = 'Kiri'
        elif selected_role == '自定义':
            st.session_state.start_info = '您好'
            st.session_state.title = '私人助手'
            st.session_state.role_prompt = st.text_area('请输入ai角色：')
        elif selected_role == '混乱模式🤯':
            st.session_state.start_info = '你惊扰了混沌......'
            st.session_state.title = '👽'
            st.session_state.role_prompt = random.choice([Zuan_role, Lyra_role, default_role])
        
        st.rerun()  # 重新运行以应用新角色
    
    st.divider()

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
            st.session_state['messages'] = []
            st.rerun()  # 刷新页面
    if clear:
        confirm_action()
    # 处理确认结果
    if st.session_state.get("confirmed"):
        st.success("数据已清空！")
        del st.session_state.confirmed


# 保存已有会话状态
if 'memory' not in st.session_state:
    st.session_state.memory = ConversationBufferWindowMemory(return_messages=True, k=5)
    st.session_state['messages'] = [{'role': 'ai','content': start_msg}]
if 'role_prompt' not in st.session_state or 'role_choice' not in st.session_state:
    st.session_state.role_choice = '默认'  # 设置默认值
    st.session_state.role_prompt = default_role
    
st.session_state.memory.chat_memory.add_ai_message(st.session_state.role_prompt)
# role_prompt = st.session_state.role_prompt

# 标题
st.title(st.session_state.title)
f'##### {st.session_state.start_info}'
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
    if not st.session_state.role_prompt:
        role_prompt = default_role
    # 保存和打印用户输入
    st.session_state['messages'].append({'role': 'human', 'content': input})
    st.chat_message('human').write(input)
    # 调用模型
    with st.spinner('ai正在思考，请稍候...'):
        response = get_chat_response(input, st.session_state['memory'], api_key, chat_model=model_name)
    # 保存和打印模型输出
    st.session_state['messages'].append({'role': 'ai', 'content': response})
    st.chat_message('role').write(response)

