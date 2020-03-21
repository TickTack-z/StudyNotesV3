import random
import pandas as pd
import numpy as np
from scipy.stats import norm 
def func1(start_point, down_point, dict_):    
    cash = 1
    equity = 0    
    for point, percent in dict_.items():
        if point < down_point:
            continue
        cash -= percent
        equity += percent/point
    return (equity*start_point+cash, equity*down_point+cash, equity, cash)

# def func1(start_point, down_point, dict_):    
#     cash = 1
#     equity = 0    
#     tot_equity = 0
#     for point, percent in dict_.items():
#         if point < down_point:
#             continue
#         cash -= percent
#         equity += percent/point
#         tot_equity += percent
#     return (tot_equity/equity, equity)

candidate = 0
candidate_val = 0
res_list = []
for z in range(50000):
    res_dict = dict()
    start_point = 2600
    cum_sum_weight = 0
    dict_ = dict(zip(list(range(1200, 2500, 100)), list(np.random.dirichlet(np.ones(13),size=1)[0])))    
    for down_point in range(2400, 1400, -50):
        if down_point == 1450:
    #         print(res_dict)
            temp = 1-sum([i[2] for i in res_dict.values()])
            tot , bot, equity, cash = func1(start_point, down_point, dict_)
            res_dict[down_point] = [tot , bot , temp, equity, cash]
            break
        tot , bot, equity, cash = func1(start_point, down_point, dict_)
        temp = (1-norm.cdf(down_point,loc=2000,scale=300) - cum_sum_weight)
        cum_sum_weight = (1-norm.cdf(down_point,loc=2000,scale=300))
        res_dict[down_point] = [tot , bot , temp, equity, cash]

    %matplotlib notebook
    df = pd.DataFrame(res_dict).T

    df.columns = ['final_asset_if_back_to_2400', 'drawdown','weight', 'equity', 'cash']
    
    cash = (df['cash']*df['weight']).sum()
    equity = (df['equity']*df['weight']).sum()
    res_list.append((cash, equity, dict_, bot))

back_to_point=2400
pain_factor = 0.05
sorted([(i[0] + i[1]*back_to_point + pain_factor*i[3], i[3], i[2]) for i in res_list], reverse = True)[0:3]
