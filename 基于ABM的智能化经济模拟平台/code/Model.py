# -*- coding: utf-8 -*-
from WorkerCompanyAgent import WorkerAgent, CompanyAgent
from BankAgent import BankAgent
from mesa import *
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from pandas import *
import numpy as np
import matplotlib.pyplot as pyplot
import sys
import time
import os
import datetime
import csv

SEQUENCE = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
SAVED_MODEL_PATH = os.path.split(os.path.abspath(__file__))[0]+"/saved_model/"+SEQUENCE+'/'
RESULT_PATH = os.path.split(os.path.abspath(__file__))[0]+"/result/"+SEQUENCE+'/'

train = 0
train_eps = 1
total_seasons = 10
rounds_per_season = 10

company_num = 20
worker_num = 1000


"""
Summary：
Model类是我们的模型，承担着调度所有Agent对象的任务；

 1、scheduler： 
    在时间上对各Agent对象进行管理；
    scheduler决定了当model.scheduler.step()调用时哪些agent对象执行agent的step（）；
    scheduler是model的一个成员属性，mesa有三个，其中RandomActivation（）是最常用的一个，
    表示每次scheduler.step()会唤醒所有的agent，并打乱agent的顺序执行agent的step（）；

 2、gird：
    在空间上对Agent对象进行管理；
    把空间划为棋盘状（width和height），并为agent赋予坐标；
    必要时可以移动，移动方式目前我只了解了随机选取临近的8个位置之一；

"""

"""
为了使用一个scheduler来管理不同类型的agent，我选取了按id号来分组的方式；
如：
全局的列表company_agent_id_list来记录company代理对象的id列表；
（每个agent有一个唯一的unique_id属性作为key值）
"""
company_agent_id_list = []
worker_agent_id_list = []

#真正控制对局的Model类
class Our_Model(Model):
    def __init__(self, N, M, width, height):
        self.company_agent_num = N
        BankAgent.set_company_num(N)
        self.worker_agent_num = M
        self.company_scheduler = RandomActivation(self)
        self.worker_scheduler = RandomActivation(self)
        self.grid = MultiGrid(width, height, True)

        #  向模型中注入agents； 安排时间和空间；
        for i in range(N):
            time.sleep(0.01)
            company_agent_id_list.append(i)
            company = CompanyAgent(i, self)
            CompanyAgent.add_company(company)
            self.company_scheduler.add(company)

        for j in range(M):
            time.sleep(0.01)
            # 记录worker的id号到全局list中
            worker_agent_id_list.append(j)
            # 添加worker到model的scheduler中
            worker = WorkerAgent(j, self)
            WorkerAgent.add_worker(worker)
            CompanyAgent.fill_talent_list(worker)
            self.worker_scheduler.add(worker)
            # 随机分配位置
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(worker, (x, y))
            CompanyAgent.fill_talent_list(worker)
            self.set_model()
        # self.data_collector =  DataCollector(
        #     agent_reporters={"Worker_Wealth": worker_wealth }
        # )

    def set_model(self):
        CompanyAgent.the_model = self
        WorkerAgent.the_model = self
    def step(self):
        #  启动一次调度
        self.company_scheduler.step()
        self.worker_scheduler.step()


#####################################################################
# 一个round有n个step； 一个轮次作为一个生产周期； 
def round(step_num, the_model):
    for i in range(step_num):
        # print("  Round {}  ".format(i).center(100, "*"))
        # print(end="\n")
        # 增加轮次计数
        if BankAgent.bankrupt == True:
            return
        BankAgent.update_round()
        print("   Round {} ".format(i).center(50, '-'), end='\n')
        the_model.step()
        if not train:
            for company_id in company_agent_id_list:
                company = the_model.company_scheduler.agents[company_id]
                company.show_company_status()
            for worker_id in worker_agent_id_list:
                worker = the_model.worker_scheduler.agents[worker_id]
                worker.show_worker_status()
        else:
            if BankAgent.get_round() == 1:
                pass
            elif BankAgent.get_round() % 3 == 1:
                WorkerAgent.worker_train()
            elif BankAgent.get_round() % 3 == 0:
                CompanyAgent.company_train()

def train_model():
    worker_moving_average_rewards = []
    company_moving_average_rewards = []
    WorkerAgent.agent_ddpg.buffer_model_load("./worker_buffer")
    CompanyAgent.agent_ddpg.buffer_model_load("./company_buffer")
    print('Start to train ! \n')
    for eps in range(train_eps):
        print("   Train eps {} ".format(eps).center(100, '~'), end='\n')
        model = Our_Model(company_num, worker_num, width=30, height=30)
        for i in range(total_seasons):
            print("   Season {} ".format(i).center(75, '*'), end='\n')
            round(rounds_per_season, model)
            if BankAgent.bankrupt == True:
                break
    print('Complete training！')
    
    WorkerAgent.agent_ddpg.buffer_model_save("./worker_buffer")
    CompanyAgent.agent_ddpg.buffer_model_save("./company_buffer")

    if not os.path.exists("./average_reward"):
        os.makedirs("./average_reward")
        record_file = open('./average_reward/average_record.csv','a', encoding='utf-8',newline="")
        csv_writer = csv.writer(record_file)
        csv_writer.writerow(["worker", "company"])
        record_file.close()

    record_file = open('./average_reward/average_record.csv','a', encoding='utf-8',newline="")
    csv_writer = csv.writer(record_file)
    csv_writer.writerow([str(WorkerAgent.agent_ddpg.memory.get_mean()), str(CompanyAgent.agent_ddpg.memory.get_mean())])
    record_file.close()

def run_model():
    worker_record_file = open('worker_record.csv','w', encoding='utf-8',newline="")
    csv_writer = csv.writer(worker_record_file)
    csv_writer.writerow(['总步数', 'ID', '总财产', '健康值', '是否工作', '工作经验' \
        , '知识值', '薪资','生产力'])
    worker_record_file.close()

    company_record_file = open('company_record.csv','w', encoding='utf-8',newline="")
    csv_writer = csv.writer(company_record_file)
    csv_writer.writerow(['总步数', 'ID', '总财产', '固定成本', '可变成本', '员工人数' \
        , '当前公司总生产力', '存货', '总负债'])
    company_record_file.close()

    origin_stdout = sys.stdout
    sys.stdout = open('output.txt', 'w')
    saved_model_path = os.path.split(os.path.abspath(__file__))[0]
    model = Our_Model(company_num, worker_num, width=30, height=30)
    WorkerAgent.agent_ddpg.load_model(saved_model_path + '/worker_buffer/target_actor_checkpoint.pth')  
    CompanyAgent.agent_ddpg.load_model(saved_model_path + '/company_buffer/target_actor_checkpoint.pth') 
    # 一个季度为10个轮次，进行5个季度；
    for i in range(total_seasons):
        print('~~'*50)
        print("   Season {} ".format(i).center(100, '*'), end='\n')
        round(rounds_per_season, model)
        if BankAgent.bankrupt == True:
            break

if __name__=='__main__':
    
    if train:
        train_model()
    else:
        run_model()
    