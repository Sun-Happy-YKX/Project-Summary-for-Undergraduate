# -*- coding: utf-8 -*-

# worker和company类相互引用，循环import解不开，只能把它们写在一个文件里
# import time
import random
import numpy as np
import pandas as pd
from functools import *
from mesa import *
from DDPG import DDPG
from BankAgent import BankAgent
from keras.models import load_model
import math
import torch
import csv


train = 0

health_decrease_rate = 0.997
basic_consume_rate = 0.6143
knowledge_increase_rate = 1.1
health_bottom = 0.3
worker_init_wealth = 10000
lowest_consume = 500
max_consume_times = 50
min_salary_per_production_means = 1000
AI_costs_to_production_magnification = 10000
AI_production_magnification = 500000
die_punish = -1000000
worker_n_states = 6
worker_n_actions = 3
worker_hidden_dim = 30
device = "cpu"

fix_costs_rate = 0.3  # 购买固定资产的花销所占企业财富值的比率
fix_costs_depreciate = 0.03  # 固定成本的折旧率
max_production_quantity_per_fix_costs = 0.1 # 后期调试 
fire_threshold = 0.2  # 当(公司现有总生产力-预期总生产力)/预期总生产力 > fire_threshold时，开始裁员
init_stock = 50000
bankrupt_punish = -10000000
company_init_wealth = 500000
company_n_states = 12
company_n_actions = 6
company_hidden_dim = 30

worker_observation_minification = [10, 50000, 1, 50, 50, 50000]
worker_action_magnification = [50000, 50000, 1]

company_observation_minification = [1000000, 100000, 100000, 500000, 100000, 10 \
    , 50000, 1000000, 100000, 100000, 500000, 100000]
company_action_magnification = [100000, 100000, 1000000, 1, 500000, 20]



class dieExcetion(RuntimeError):
    def __init__(self, arg):
        self.args = arg

class WorkerAgent(Agent):
    # 类变量：总执行数，用来对worker的生产经验进行归一化
    __all_worker_list = []
    the_model = None
    agent_ddpg = DDPG(worker_n_states, worker_n_actions, worker_hidden_dim, memory_capacity=200000, batch_size=256)
    def __init__(self, agent_id, model):
        super().__init__(agent_id, model)

        self.total_steps = 0
        self.noise = np.random.normal(loc=0.0, scale=1, size=(1, worker_n_actions))
        self.wealth = worker_init_wealth * random.uniform(0.8, 1.2)
        self.health = 1
        self.is_working = False
        self.want_to_work = True
        self.working_company = None
        # self.ability = ABILITY_LOW
        self.company_id = None
        # working_experience 是一个人的生产力的重要一项；另一项是健康值；
        self.working_experience = 1
        self.knowledge = 1
        self.salary = 0

        self.production_means = 0

        self.AI_step_params = {}
        self.reward = 0    # 相邻两回合间的差值才是真正的reward
        self.data_memory = []

    @classmethod
    def clean_class_variables(cls):
        __all_worker_list = []
        the_model = None
    @classmethod
    def get_worker_list(cls):
        return cls.__all_worker_list

    @classmethod
    def add_worker(cls, worker):
        cls.__all_worker_list.append(worker)

    @classmethod
    def worker_train(cls):
        cls.agent_ddpg.update()

    def push_data_into_memory(self):
        if self.total_steps == 1:
            self.reward = self.get_reward()
            return
        elif self.total_steps % 3 == 1:
            for i in range(len(self.data_memory) - 1):
                WorkerAgent.agent_ddpg.memory.push(self.data_memory[i][0], self.data_memory[i][1] \
                    , self.data_memory[i][2], self.data_memory[i + 1][0], False)
            WorkerAgent.agent_ddpg.memory.push(self.data_memory[len(self.data_memory) - 1][0], self.data_memory[len(self.data_memory) - 1][1] \
                , self.data_memory[len(self.data_memory) - 1][2], np.array(self.get_observation()), False)
            self.data_memory = []
        reward = self.get_reward() - self.reward
        self.reward = self.get_reward()
        self.data_memory.append([np.array(self.get_observation()) \
            , np.array(list(self.AI_step_params.values())), reward])

    def get_AI_step_params(self):
        observation = np.array(self.get_observation())
        action = WorkerAgent.agent_ddpg.select_action(observation)
        if train:
            action = np.array(WorkerAgent.agent_ddpg.select_action(observation)) + self.noise[0]
        action = abs(action)
        # action = 1 * (action >= 0) * action
        self.AI_step_params['save_money'] = action[0] * worker_action_magnification[0]
        self.AI_step_params['withdraw_money'] = action[1] * worker_action_magnification[1]
        self.AI_step_params['choose_to_educate'] = action[2] * worker_action_magnification[2]

    def get_reward(self):
        save_money = BankAgent.cal_worker_money(self.unique_id)
        # return (self.wealth + save_money) * self.cal_production_means()
        return self.wealth + save_money

    def get_observation(self):
        average_production_means = sum([worker.production_means for worker in WorkerAgent.get_worker_list()])/len(WorkerAgent.get_worker_list())
        average_salary = sum([worker.salary for worker in WorkerAgent.get_worker_list()])/len(WorkerAgent.get_worker_list())
        
        max_salary = 0
        company_recruit_infor_list = sorted(
            list(
              (company, min(self.production_means/company.production_means_needed, 1)*company.salary_can_offer) 
              for company in CompanyAgent.get_company_list() if company.production_means_needed > 0
            ), key=lambda item: -1*item[1]
        )
        if company_recruit_infor_list:
            max_salary = company_recruit_infor_list[0][1]

        observation = [average_production_means \
            , average_salary, self.health, self.knowledge, self.working_experience, max_salary]
        for i in range(len(observation)):
            observation[i] = observation[i] / worker_observation_minification[i]
        return observation

    # 用于招聘时，计算talent_list中的待业人员的生产力
    def cal_production_means(self):
        result = math.log(self.working_experience * self.knowledge * self.health + 1)
        return round(result, 4)

    def apply_for_job(self):
        # (company, 该worker在该公司剩余职位条件下可以得到的薪资)
        company_recruit_infor_list = sorted(
            list(
              (company, min(self.production_means/company.production_means_needed, 1)*company.salary_can_offer) 
              for company in CompanyAgent.get_company_list() if company.production_means_needed > 0
            ), key=lambda item: -1*item[1]
        )
        # print("dudu!", [item[1] for item in company_recruit_infor_list])
        if not company_recruit_infor_list:
            return
        if company_recruit_infor_list[0][1] < self.cal_production_means() * min_salary_per_production_means:
            return
        self.salary = company_recruit_infor_list[0][1]
        if self.salary != 0:
            company = company_recruit_infor_list[0][0]
            company.recruit_worker(self)       
        
        
    # 向银行存款 
    def save_money_to_bank(self):
        BankAgent.worker_save_money(self.unique_id, self.AI_step_params['save_money'])
        self.wealth -= self.AI_step_params['save_money']

    # 从银行取钱 
    def withdraw(self):
        withdraw_money = BankAgent.worker_back_money(self.unique_id, self.AI_step_params['withdraw_money'])
        self.wealth += withdraw_money
        self.withdraw_money = withdraw_money

    # 购买某一公司的货物
    def buy_products(self):
        consuming = self.salary * basic_consume_rate* random.uniform(0.5, 1.5)+lowest_consume  #消费量，需要机器学习
        consume_times = 0
        while consuming > 0 and consume_times < max_consume_times:
            consume_times += 1
            company_agent_list = CompanyAgent.get_company_list()
            supply_company = random.choice(company_agent_list)
            if consuming > self.wealth:
                raise dieExcetion("Worker die")
                self.die()
                return
            if consuming > supply_company.stock:
                self.wealth -= supply_company.stock
                consuming -= supply_company.stock
                supply_company.stock = 0
            else:
                self.wealth -= consuming
                supply_company.stock -= consuming
                consuming = 0
        

    # 选择教育后要做的事
    def choose_education(self):
        if self.is_working:
            self.working_company.employee_list.remove(self)
            CompanyAgent.fill_talent_list(self)
        self.is_working = False
        self.knowledge *= knowledge_increase_rate
        self.wealth *= random.uniform(0.95, 0.98)
    
    # 是否选择教育
    def get_education(self):
        if self.AI_step_params['choose_to_educate'] < 0.5:
            self.choose_education()
            return True
        else:
            return False

    # 选择医疗后要做的事    
    def heal(self):
        addtion = random.uniform(health_bottom, health_bottom+0.3)
        if self.wealth < addtion*worker_init_wealth:
            addtion = self.wealth/(2*worker_init_wealth)
        self.wealth -= addtion * worker_init_wealth
        self.health += addtion
        
    # 若判定该角色死亡，要做的事
    def die(self):
        if self.is_working:
            self.working_company.employee_list.remove(self)
        CompanyAgent.get_talent_list().remove(self)
        WorkerAgent.get_worker_list().remove(self)
        WorkerAgent.the_model.worker_scheduler.remove(self)
        
        reward = die_punish
        for i in range(len(self.data_memory) - 1):
            WorkerAgent.agent_ddpg.memory.push(self.data_memory[i][0], self.data_memory[i][1] \
                , self.data_memory[i][2], self.data_memory[i + 1][0], False)
        WorkerAgent.agent_ddpg.memory.push(self.data_memory[len(self.data_memory) - 1][0] \
            , self.data_memory[len(self.data_memory) - 1][1], reward, np.array(self.get_observation()), True)
        self.data_memory = []

    def step(self) -> None:

        self.total_steps += 1
        self.production_means = self.cal_production_means()
        self.get_AI_step_params()
        if train:
            self.push_data_into_memory()
        try:
            self.withdraw() # 取钱
            # 给公司分配初始员工
            # if self.total_steps == 1:
            #     if random.uniform(0, 1) > 0.4:
            #         company = random.sample(CompanyAgent.get_company_list(), 1)[0]
            #         self.salary = company.AI_step_params['total_salary'] / 30
            #         company.recruit_worker(self)

            if not self.get_education():
                if not self.is_working:
                    self.apply_for_job()
                
            self.buy_products()
            self.save_money_to_bank()

            if self.is_working:
                self.health *= health_decrease_rate + random.uniform(-0.001, 0.001)
                
            if self.health < health_bottom:
                self.heal()
        except dieExcetion as e:
            return
               
    def show_worker_status(self):
        print("*" * 50)
        print("Worker {} status: ".format(self.unique_id))
        print((" IS_Working: {0:<2} \n Health: {1:<2} \n Working_Experience: {2:<5.2f} \n Knowledge" + \
        ": {3:<.2f} \n Salary: {4:<7.2f} \n Wealth: {5:<4.2f}$ \n Production_Means: {6:<5.4}")
            .format(self.is_working, self.health, self.working_experience, self.knowledge, self.salary, self.wealth, self.production_means))
        print(("Withdraw Money: {0:<2}").format(self.withdraw_money))
        print(self.AI_step_params)

        record_file = open('worker_record.csv','a', encoding='utf-8',newline="")
        csv_writer = csv.writer(record_file)
        csv_writer.writerow([str(self.total_steps) \
            , str(self.unique_id) \
            , str(self.wealth) \
            , str(self.health) \
            , str(self.is_working) \
            , str(self.working_experience) \
            , str(self.knowledge) \
            , str(self.salary) \
            , str(self.production_means)])
        record_file.close()

#####################################################################################


# 公司 继承自agent
class CompanyAgent(Agent):
    the_model = None
    __talent_list = []  # 人才市场； 用于招聘；
    __company_list = []  # 存储公司对象
    production_model = load_model("production_model.h5")
    agent_ddpg = DDPG(company_n_states, company_n_actions, company_hidden_dim, memory_capacity=4000, batch_size=128)
    
    @classmethod
    def clean_class_variables(cls):
        __talent_list = []
        __company_list = []
        the_model = None

    # 获取公司对象
    @classmethod
    def get_company_list(cls):
        return cls.__company_list

    # 向company_list中添加公司对象
    @classmethod
    def add_company(cls, c):
        cls.__company_list.append(c)

    # 人才市场列表
    @classmethod
    def get_talent_list(cls):
        return cls.__talent_list

    # 增加可招聘员工
    @classmethod
    def fill_talent_list(cls, worker_agent):
        cls.__talent_list.append(worker_agent)

    @classmethod
    def company_train(cls):
        cls.agent_ddpg.update()

#  添加成员变量--生产和消费；
    def __init__(self, id, model, name=None, FixedCosts=0, VariableCosts=0):
        super().__init__(id, model)

        self.total_steps = 0
        
        self.noise = np.random.normal(loc=0.0, scale=1, size=(1, company_n_actions))

        self.name = name
        # 固定成本
        self.fixed_costs = FixedCosts
        # 可变成本
        self.variable_costs = VariableCosts
        self.wealth = company_init_wealth * random.uniform(0.8, 1.2)
        # 员工列表
        self.employee_list = []
        self.last_round_wealth = self.wealth
        # self.credit = 1  # 公司的信用，【0-1】
        # self.max_employee_num
        self.operating_cost = 0 # 该轮次的营业成本
        self.income = 0  # 该轮次的营业收入
        self.profit = 0  # 该轮利润
        self.stock = init_stock * random.uniform(0.8, 1.2)  # 该轮结束后的存货量
        self.Production = 0

        self.AI_step_params = {}
        self.reward = 0    # 相邻两回合间的差值才是真正的reward
        self.data_memory = []

    def push_data_into_memory(self):
        if self.total_steps == 1:
            self.reward = self.get_reward()
            return
        elif self.total_steps % 3 == 0:
            for i in range(len(self.data_memory) - 1):
                CompanyAgent.agent_ddpg.memory.push(self.data_memory[i][0], self.data_memory[i][1] \
                    , self.data_memory[i][2], self.data_memory[i + 1][0], False)
            CompanyAgent.agent_ddpg.memory.push(self.data_memory[len(self.data_memory) - 1][0], self.data_memory[len(self.data_memory) - 1][1] \
                , self.data_memory[len(self.data_memory) - 1][2], np.array(self.get_observation()), False)
            self.data_memory = []
        if 'production' in self.AI_step_params:
            del self.AI_step_params['production']
        reward = self.get_reward() - self.reward
        self.reward = self.get_reward()
        self.data_memory.append([np.array(self.get_observation()) \
            , np.array(list(self.AI_step_params.values())), reward])

    def get_AI_step_params(self):
        observation = np.array(self.get_observation())
        action = CompanyAgent.agent_ddpg.select_action(observation)
        if train:
            action = np.array(CompanyAgent.agent_ddpg.select_action(observation)) + self.noise[0]
        # action = 1 * (action >= 0) * action
        action = abs(action)
        self.AI_step_params['fixed_costs'] = action[0] * company_action_magnification[0]
        self.AI_step_params['variable_costs'] = action[1] * company_action_magnification[1]
        self.AI_step_params['total_salary'] = action[2] * company_action_magnification[2]
        self.AI_step_params['choose_to_loan'] = action[3] * company_action_magnification[3]
        self.AI_step_params['loan_money'] = action[4] * company_action_magnification[4]
        self.AI_step_params['loan_round'] = max(math.ceil(action[5] * company_action_magnification[5]), 1)
    
    def get_reward(self):
        return self.wealth - BankAgent.get_remain_debt(self.unique_id)

    def get_observation(self):
        average_wealth = sum([company.wealth for company in CompanyAgent.get_company_list()])/len(CompanyAgent.get_company_list())
        average_fixed_cost = sum([company.fixed_costs for company in CompanyAgent.get_company_list()])/len(CompanyAgent.get_company_list())
        average_variable_cost = sum([company.variable_costs for company in CompanyAgent.get_company_list()])/len(CompanyAgent.get_company_list())
        average_debt = sum([BankAgent.get_remain_debt(company.unique_id) for company in CompanyAgent.get_company_list()])/len(CompanyAgent.get_company_list())
        average_stock = sum([company.stock for company in CompanyAgent.get_company_list()])/len(CompanyAgent.get_company_list())
        average_production_means = sum([worker.production_means for worker in WorkerAgent.get_worker_list()])/len(WorkerAgent.get_worker_list())
        average_salary = sum([worker.salary for worker in WorkerAgent.get_worker_list()])/len(WorkerAgent.get_worker_list())
        observation = [average_wealth, average_fixed_cost, average_variable_cost, average_debt, average_stock \
            , average_production_means, average_salary, self.wealth, self.fixed_costs, self.variable_costs \
            , BankAgent.get_remain_debt(self.unique_id), self.stock]
        for i in range(len(observation)):
            observation[i] = observation[i] / company_observation_minification[i]
        return observation

    def fixed_costs_depreciate(self):
        self.fixed_costs *= (1 - fix_costs_depreciate) * random.uniform(0.95, 1.05)

    # 购买固定资产
    def purchase_fixed_costs(self):
        total_needed_fix_costs = self.AI_step_params['fixed_costs']
        if total_needed_fix_costs > self.fixed_costs:
            cost = total_needed_fix_costs - self.fixed_costs
            if self.wealth > cost:
                self.fixed_costs = total_needed_fix_costs
                self.wealth -= cost
            else:
                self.fixed_costs += self.wealth
                self.wealth = 0


    def purchase_variable_costs(self):
        total_needed_variable_costs = self.AI_step_params['variable_costs']
        if total_needed_variable_costs > self.variable_costs:
            cost = total_needed_variable_costs - self.variable_costs
            if self.wealth > cost:
                self.variable_costs = total_needed_variable_costs
                self.wealth -= cost
            else:
                self.variable_costs += self.wealth
                self.wealth = 0

    def pay_salary(self):
        for employee in self.employee_list:
            employee.working_experience += 1
            if self.wealth >= employee.salary:
                employee.wealth += employee.salary
                self.wealth -= employee.salary
            else:
                employee.wealth += self.wealth
                self.wealth = 0
                raise dieExcetion("Company bankrupt")
                self.bankruptcy()

    # 招入某位worker
    def recruit_worker(self, worker):
        worker.is_working = True
        worker.working_company = self
        self.employee_list.append(worker)
        CompanyAgent.get_talent_list().remove(worker)
        self.production_means_needed -= worker.production_means
        self.salary_can_offer -= worker.salary
    
    # 有待完善
    def get_production_means_by_production(self):
        return self.AI_step_params['production'] / 10000
    # AI给出招聘信息
    def recruit_information(self):
        costs = np.array([[self.fixed_costs * AI_costs_to_production_magnification, \
            self.variable_costs * AI_costs_to_production_magnification]])
        get_production = CompanyAgent.production_model.predict(costs)
        baseline = CompanyAgent.production_model.predict(np.array([[1, 1]]))
        predict_result = 0
        if baseline[0][0] >= get_production[0][0]:
            predict_result = 0
        else:
            predict_result = get_production[0][0] - baseline[0][0]
        self.AI_step_params['production'] = predict_result * AI_production_magnification

        self.production_means_predicted = self.get_production_means_by_production()
        # self.AI_step_params['production'] * rate_production_means_per_production

        self.production_means_needed = \
            self.production_means_predicted - sum([employee.production_means for employee in self.employee_list])
        self.total_salary_can_offer = self.AI_step_params['total_salary']
        self.salary_can_offer = \
            self.total_salary_can_offer - sum([employee.salary for employee in self.employee_list])
        if self.production_means_needed <= 0 or self.salary_can_offer <= 0:
            self.production_means_needed = 0
            self.salary_can_offer = 0
     
    

    def fire(self):
        while True:
            total_production_means = sum([worker.production_means for worker in self.employee_list])
            total_salary = sum([worker.salary for worker in self.employee_list])
            if self.production_means_predicted == 0 or self.total_salary_can_offer == 0:
                break
            if total_production_means/self.production_means_predicted <= 1 + fire_threshold\
                and total_salary/self.total_salary_can_offer <= 1 + fire_threshold:
                break 
            fire_value = [1/worker.production_means for worker in self.employee_list]
            sum_fire_value = sum(fire_value)
            fire_rate = list(map(lambda item:item/sum_fire_value, fire_value))
            fire_random_needle = random.random()      #随机投针，完成"按概率解聘"的操作
            temp_boundary = 0
            for i in range(len(fire_rate)):
                worker = self.employee_list[i]
                temp_boundary += fire_rate[i]
                if fire_random_needle <= temp_boundary:
                    self.fire_worker(worker)
                    break
        
    
    def fire_worker(self, worker):
        self.employee_list.remove(worker)
        worker.is_working = False
        CompanyAgent.get_talent_list().append(worker)
        # 本来就是处于生产力过剩状态才进行解聘，所以不改动招聘相关信息(因为没必要招聘了)

    def show_company_status(self):
        print("\n")
        print("*"*100)
        print("Total steps: {}".format(self.total_steps))
        print("Company {} status: ".format(self.unique_id))
        print("Wealth: {0:.2f}\nFixedCosts: {1:.2f}\nVariableCosts: {2:.2f}\nStock:{3:.2f}" \
            .format(self.wealth, self.fixed_costs, self.variable_costs, self.stock))
        print("Employee_list: ",sorted(list(x.unique_id for x in self.employee_list)) )
        print("Employee Number: {}".format(len(self.employee_list)))
        all_employee_salary = sum(list(x.salary for x in self.employee_list ))
        print("All Employee's Salary is: {:.2f}".format(all_employee_salary))
        # 一个worker的生产力暂定为他的working_experience*0.75 + health*0.25
        # 下面的sum求的就是这个公司的所有在职员工的总生产力
        total_prodution_means = sum(list(x.production_means for x in self.employee_list))
        print("Total production_means: {:.4f}".format(total_prodution_means))
        print("Total Debt: {:.2f}".format(BankAgent.get_remain_debt(self.unique_id)))
        print("Total_production_means_needed: {:.4f}".format(self.production_means_predicted))
        print("Total salary: {:.4f}".format(self.AI_step_params['total_salary']))
        print(self.AI_step_params)
        print("*"*100)
        print('\n')

        record_file = open('company_record.csv','a', encoding='utf-8',newline="")
        csv_writer = csv.writer(record_file)
        csv_writer.writerow([str(self.total_steps) \
            , str(self.unique_id) \
            , str(self.wealth) \
            , str(self.fixed_costs) \
            , str(self.variable_costs) \
            , str(len(self.employee_list)) \
            , str(total_prodution_means) \
            , str(self.stock) \
            , str(BankAgent.get_remain_debt(self.unique_id))])

        record_file.close()


    def produce(self):
        if self.AI_step_params['production'] == 0:
            self.Production = 0
            return
        self.Production = min(self.AI_step_params['production'] \
                          * sum([worker.production_means for worker in self.employee_list]) \
                          / self.production_means_predicted, self.AI_step_params['production'])
        self.stock += self.Production
        self.variable_costs = self.variable_costs * (1 - min(self.Production / self.AI_step_params['production'], 1))


    # 向银行贷款 ok
    def loan_money_from_bank(self):

        if self.AI_step_params['choose_to_loan'] < 0.5:

            loan_money = self.AI_step_params['loan_money']
            loan_round = self.AI_step_params['loan_round']
            get_loan_money = BankAgent.company_loan_money(self.unique_id, loan_money, loan_round)
            # 如果银行不接受贷款，得到的贷款数会是0，因此可以直接相加
            self.wealth += get_loan_money

    # 到时间了得还钱
    def repay_loan(self):
        # 如果无需还钱,repay_money值将为0, 故可不经条件判断直接运算
        repay_money = BankAgent.need_to_repay(self.unique_id)
        if self.wealth >= repay_money:
            self.wealth -= repay_money
            BankAgent.company_repay(self.unique_id, repay_money)
        else:
            raise dieExcetion("Company bankrupt")
            self.bankruptcy()

    def bankruptcy(self):
        for employee in self.employee_list:
            self.fire_worker(employee)
        CompanyAgent.get_company_list().remove(self)
        CompanyAgent.the_model.company_scheduler.remove(self)

        reward = bankrupt_punish
        for i in range(len(self.data_memory) - 1):
            CompanyAgent.agent_ddpg.memory.push(self.data_memory[i][0], self.data_memory[i][1] \
                , self.data_memory[i][2], self.data_memory[i + 1][0], False)
        CompanyAgent.agent_ddpg.memory.push(self.data_memory[len(self.data_memory) - 1][0] \
            , self.data_memory[len(self.data_memory) - 1][1], reward, np.array(self.get_observation()), True)
        self.data_memory = []     

    # company一次操作
    def step(self) -> None:
        try:
            # time.sleep(1)
            self.total_steps += 1
            self.get_AI_step_params()
            if train:
                self.push_data_into_memory()
            self.loan_money_from_bank()
            self.purchase_fixed_costs()
            self.purchase_variable_costs()
            self.last_round_wealth = self.wealth
            self.recruit_information()
            self.fire()
            self.produce()   
            self.pay_salary()
            self.repay_loan()
        except dieExcetion as e:
            return
        
