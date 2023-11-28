def init_prompt(messages):
    content = '你是一名具备数据分析能力的场景营销人员，能够给予一些数据从表中提取数据并进行解读。'
    message = {
        "role": "system",
        "content": content
    }
    messages.append(message)
    return messages

def scenario_cate_prompt(messages, user_content, scenario_cate_list):
    content = f"""
    {user_content}

    请你推荐四个最相关的场景类型，并说明理由。
    注意：此部分数据从下述场景列表中生成，场景列表中的数据是使用,隔开的，不能自己生成。
    输出格式为：用选择出得场景名称替换xxx，理由替换XXX
        1. xxx：XXX
        2. xxx：XXX
        3. xxx：XXX
        4. xxx：XXX

    场景列表：{scenario_cate_list}
    """
    message = {
        "role": "user",
        "content": content
    }
    messages.append(message)
    return messages


def scenario_cate_tuning_prompt(messages, user_content, scenario_cate_list):
    content = f"""
    {user_content}

    请你推荐四个最相关的场景类型，并说明理由。
    注意：此部分数据从下述场景列表中生成，场景列表中的数据是使用,隔开的，不能自己生成。
    输出格式为：用选择出得场景名称替换xxx，理由替换XXX
        1. xxx：XXX
        2. xxx：XXX
        3. xxx：XXX
        4. xxx：XXX

    场景列表：{scenario_cate_list}
    """
    message = {
        "role": "user",
        "content": content
    }
    messages.append(message)
    return messages