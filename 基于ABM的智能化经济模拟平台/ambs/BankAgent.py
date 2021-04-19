from mesa import *
import random

# 不知道能不能调用model，需要company_agent_id_list
bank_money_remain_rate = 0.11

class BankAgent(Agent):
    # 记录公司总数
    company_num = 0
    # 记录轮次
    round = 0
    worker_save_record = {} # 工人存款记录单
    company_loan_record = {}  # 公司贷款记录单
    
    init_wealth = 100000000
    wealth = 100000000
    save_rate = 0.01
    loan_rate = 0.05
    bankrupt = False

    def __init__(self, model):
        super().__init__(id, model)
        # 需要预留一部分支付存款
        # self.store_wealth = self.wealth
        # 存款利率和贷款利率

    @classmethod
    def clean_class_variables(cls):
        # 记录公司总数
        cls.company_num = 0
        # 记录轮次
        cls.round = 0
        cls.worker_save_record = {} # 工人存款记录单
        cls.company_loan_record = {}  # 公司贷款记录单
        
        cls.init_wealth = 100000000
        cls.wealth = 100000000
        cls.save_rate = 0.01
        cls.loan_rate = 0.05
        cls.bankrupt = False

    @classmethod
    def set_company_num(cls, num):
        cls.company_num = num

    # 更新轮次，用于活期存储时记录天数
    @classmethod
    def update_round(cls):
        cls.round += 1
    @classmethod
    def get_round(cls):
        return cls.round
    """
    1. 工人存款
    2. 判断并取款（要没法给工人钱的话就不行了）
    记录【存款单号】【工人id】【金额】【存款的时间点】（暂时选择活期存储）
    暂时存款利率是固定的
    """

    @classmethod
    # 用利率和轮次计算利息和本金总和
    def cal_worker_money(cls, worker_id):
        if worker_id not in cls.worker_save_record:
            return 0
        basic_money = cls.worker_save_record[worker_id][0]
        save_round = cls.round - cls.worker_save_record[worker_id][1]
        rate = cls.save_rate
        return (rate + 1) * basic_money * save_round

    # 工人存钱
    @classmethod
    def worker_save_money(cls, save_id, money):
        cls.wealth += money
        # 最后一个参数记录当前轮次
        if save_id in cls.worker_save_record:
            basic_money = BankAgent.cal_worker_money(save_id)
            cls.worker_save_record[save_id][0] = basic_money + money
            cls.worker_save_record[save_id][1] = cls.round
        else:
            lst = [money, cls.round]
            cls.worker_save_record[save_id] = lst

    # 工人取回存款
    @classmethod
    def worker_back_money(cls, save_id, money):
        
        if save_id in cls.worker_save_record:
            basic_money = BankAgent.cal_worker_money(save_id)
            if basic_money > money:
                cls.worker_save_record[save_id][0] = basic_money - money
                cls.worker_save_record[save_id][1] = cls.round
                if cls.wealth >= money:
                    return money
                else:
                    print("Bank Fail!")
                    cls.bankrupt = True
                    return cls.wealth

            else:
                cls.worker_save_record[save_id][0] = 0
                cls.worker_save_record[save_id][1] = cls.round
                if cls.wealth >= basic_money:
                    return basic_money
                else:
                    print("Bank Fail!")
                    cls.bankrupt = True
                    return cls.wealth             
        else:
            return 0
       
    """
    公司贷款
    1. 要先判断能不能贷给这个公司——根据公司情况？银行钱够不够？
    2. 贷款
    3. 收款
    记录【贷款单号】【公司id】【金额】【贷款时的时间点】【贷款年限】
    """

    # 能不能贷？
    @classmethod
    def accept_loan(cls, company_id, money):
        if not money <= cls.init_wealth*(1-bank_money_remain_rate)/cls.company_num * random.uniform(0.9,1.1):
            return False
        if cls.need_to_repay(company_id) > 0:
            return False
        if money > cls.wealth:
            return False
        return True

    @classmethod
    def get_remain_debt(cls, company_id):
        if company_id not in cls.company_loan_record:
            return 0
        repay_money_per_round = cls.company_loan_record[company_id][0]/cls.company_loan_record[company_id][2]
        return repay_money_per_round * (cls.company_loan_record[company_id][2] - cls.company_loan_record[company_id][3])

    @classmethod
    def need_to_repay(cls, company_id):
        if company_id not in cls.company_loan_record:
            return 0        
        repay_money = cls.company_loan_record[company_id][0]/cls.company_loan_record[company_id][2]
        if cls.company_loan_record[company_id][2] == cls.company_loan_record[company_id][3]:
            return 0
        return repay_money
    @classmethod
    def cal_total_loan_of_a_company(cls, company_id):
        rate = cls.loan_rate
        return (rate + 1) * cls.company_loan_record[company_id][0] * (cls.round - cls.company_loan_record[company_id][1])

    # 贷款给公司
    # 这里设定公司主动给银行还款
    # 不知道更新要不要改为银行向公司要求还贷，这样需要用一个列表存储公司对象
    @classmethod
    def company_loan_money(cls, company_id, money, loan_round):
        if cls.accept_loan(company_id, money):
            the_round_company_have_repaid = 0
            cls.company_loan_record[company_id] = [money, cls.round, loan_round, the_round_company_have_repaid]
            cls.wealth -= money
            return money
        else:
            return 0

    # 时间到了【需要在外面判断】需要向公司要钱
    @classmethod
    def company_repay(cls, company_id, repay_money):
        if company_id not in cls.company_loan_record:
            return
        cls.wealth += repay_money
        cls.company_loan_record[company_id][3] += 1
