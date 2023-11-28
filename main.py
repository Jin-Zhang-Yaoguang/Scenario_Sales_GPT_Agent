import pandas as pd
import numpy as np

from utils.prompt import init_prompt, scenario_cate_prompt
from utils.meta_data import dim_scenario_dianping_poi_ddl
from utils.GPT_agents import chat_gpt_agent, sc_agent


def main():
    flag, count, parse, messages = 1, 1, 1, []

    scenario_cate_file = 'data/场景类型.xlsx'
    scenario_file = 'data/场景列表.csv'
    scenario_cate_file = pd.read_excel(scenario_cate_file)
    scenario_cate_list = ','.join(scenario_cate_file['场景二级类目'].to_list())


    while flag:

        user_msg = input('User：')
        print('')

        # 判断是否结束
        if user_msg == '':
            flag = 0
            break

        if user_msg == '确定场景类型':
            parse += 1
            select_sc = parts
            db_meta = dim_scenario_dianping_poi_ddl
            user_msg = '找出选中类目中最受欢迎的100个场景，一共输出100个有效场景，提供每个场景的店铺名称、地址\r\n'
            user_msg += select_sc

            print('已确定场景类型')
            print(user_msg)

            sc_agent(db_meta, user_msg)


        # 初始化：预置prompt、本地数据库连接
        if parse == 1:
            if count == 1:
                messages = init_prompt(messages)
                messages = scenario_cate_prompt(messages, user_msg, scenario_cate_list)
            else:
                messages = scenario_cate_prompt(messages, user_msg, scenario_cate_list)
            messages,parts = chat_gpt_agent(messages)


        if parse == 2:
            sc_agent(db_meta, user_msg)
        count += 1


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
