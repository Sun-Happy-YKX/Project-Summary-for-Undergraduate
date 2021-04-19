# -*- coding: utf-8 -*-
"""
MyProblem.py
该案例展示了一个简单的连续型决策变量最大化目标的单目标优化问题。
max f = x * np.sin(10 * np.pi * x) + 2.0
s.t.
-1 <= x <= 2
"""

import numpy as np
import geatpy as ea


class MyProblem(ea.Problem):  # 继承Problem父类
    def __init__(self):
        name = 'MyProblem'  # 初始化name（函数名称，可以随意设置）
        M = 1  # 初始化M（目标维数）
        maxormins = [-1]  # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）
        Dim = 2  # 初始化Dim（决策变量维数）
        varTypes = [0] * Dim  # 初始化varTypes（决策变量的类型，元素为0表示对应的变量是连续的；1表示是离散的）
        lb = [-3, 4.1]  # 决策变量下界
        ub = [12.1, 5.8]  # 决策变量上界
        lbin = [1] * Dim  # 决策变量下边界
        ubin = [1] * Dim  # 决策变量上边界
        # 调用父类构造方法完成实例化
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)

    def aimFunc(self, pop):  # 目标函数
        x1 = pop.Phen[:, [0]]  # 获取表现型矩阵的第一列，得到所有个体的x1的值
        x2 = pop.Phen[:, [1]]
        f = 21.5 + x1 * np.sin(4 * np.pi * x1) + x2 * np.sin(20 * np.pi * x2)
        exIdx1 = np.where(x1 == 10)[0]  # 因为约束条件之一是x1不能为10，这里把x1等于10的个体找到
        exIdx2 = np.where(x2 == 5)[0]
        pop.CV = np.zeros((pop.sizes, 2))
        pop.CV[exIdx1, 0] = 1
        pop.CV[exIdx2, 1] = 1
        pop.ObjV = f  # 计算目标函数值，赋值给pop种群对象的ObjV属性
