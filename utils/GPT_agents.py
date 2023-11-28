### chat enginner
# Assistants API
# Import the os package
import os

# Import the openai package
import openai

import pandas as pd
from tqdm import tqdm

from openai import OpenAI
import time


def chat_gpt_agent(messages):
    client = OpenAI(
        api_key='xxx'
    )

    chat_completion = client.chat.completions.create(
        messages=messages,
        model="gpt-4",
        stream=True
    )

    parts = []
    for part in chat_completion:
        print(part.choices[0].delta.content or "", end='')
        parts.append(part.choices[0].delta.content or "")

    print('')
    print('')

    content = ''.join(parts)

    message = {
        "role": "assistant",
        "content": content
    }
    messages.append(message)
    return messages, content


def sc_agent(db_meta, user_msg):
    client = OpenAI(
        api_key='xxx'
    )

    scenario_cate_file = 'data/场景类型.xlsx'
    scenario_file = 'data/场景列表.csv'

    # 第 1 步：创建助手（Assistant)和文件
    scenario_file = client.files.create(
        file=open(scenario_file, "rb"),
        purpose='assistants'
    )

    assistant = client.beta.assistants.create(
        name="scenario sales",
        instructions="你是一名具备数据分析能力的场景营销人员，能够给予一些数据从表中提取数据并进行解读。",
        tools=[{"type": "code_interpreter"}],
        model="gpt-4-1106-preview",
        file_ids=[scenario_file.id]
    )

    # 第 2 步：创建线程（Thread）
    # 一个线程代表一个对话。我们建议在用户发起对话后立即为每个用户创建一个线程。通过创建 Messages在此线程中传递任何特定于用户的上下文和文件。
    thread = client.beta.threads.create()

    # 第 3 步：向线程添加消息（Message）
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=f"""
        提供的csv数据文件是从数据库中导出的，数据库的表结构为
        {db_meta}


        请你使用pandas将数据文件读入，并在下面的类目中，{user_msg}
        
        注意：全程使用中文回答
        """,
        file_ids=[scenario_file.id]
    )

    # 第 4 步：运行助手
    # 为了让助手响应用户消息，您需要创建一个 Run。这使得助手读取线程并决定是调用工具（如果启用了）还是简单地使用模型来最好地回答查询。
    # 随着运行的进行，助手将消息附加到带有role="assistant". 助手还将自动决定要在模型的上下文窗口中包含哪些先前的消息。
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        tools=[{"type": "code_interpreter"}, {"type": "retrieval"}]
    )

    # 第 5 步：等待完成
    flag = 1
    while flag:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        time.sleep(1)
        if run.__dict__['status'] == 'completed':
            flag = 0

    # 第 6 步：显示助手的响应
    # 运行完成后，您可以列出助手添加到线程的消息。
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )

    # 输出返回结果
    for i in range(len(messages.__dict__['data']) - 2, -1, -1):
        print(messages.__dict__['data'][i].__dict__['content'][0].__dict__['text'].__dict__['value'])


    # 整理sql
    run_steps = client.beta.threads.runs.steps.list(
        thread_id=thread.id,
        run_id=run.id
    )

    # code = []

    # for i in range(len(run_steps.__dict__['data']), -1, -1):
    #     try:
    #
    #         code += run_steps.__dict__['data'][i].__dict__['step_details'].__dict__['tool_calls'][0].__dict__[
    #             'code_interpreter'].__dict__['input'].split('\r\n')
    #     except:
    #         pass
    #
    # code = [i[:12] != 'file_path = ' and i or f"file_path = 'data/场景列表.csv'" for i in code]
    # code[-1] = "result=" + code[-1]
    # code_str = '\n'.join(code)
    # # 创建一个字典来存储局部变量
    # local_variables = {}
    # exec(code_str, globals(), local_variables)
    #
    # # 从局部变量中获取结果
    # result = local_variables['result']
    # result
