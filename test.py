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
    return (equity*start_point+cash, equity*down_point+cash)

candidate = 0
candidate_val = 0
for z in range(10000):
    res_dict = dict()
    start_point = 2450
    cum_sum_weight = 0
    dict_ = dict(zip(list(range(1200, 2400, 100)), list(np.random.dirichlet(np.ones(12),size=1)[0])))    
    for down_point in range(2400, 1400, -50):
        if down_point == 1450:
    #         print(res_dict)
            temp = 1-sum([i[2] for i in res_dict.values()])
            tot , bot = func1(start_point, down_point, dict_)
            res_dict[down_point] = [tot , bot , temp]        
            break
        tot , bot = func1(start_point, down_point, dict_)
        temp = (1-norm.cdf(down_point,loc=1850,scale=300) - cum_sum_weight)
        cum_sum_weight = (1-norm.cdf(down_point,loc=1850,scale=300))
        res_dict[down_point] = [tot , bot , temp]

    %matplotlib notebook
    df = pd.DataFrame(res_dict).T

    df.columns = ['final_asset_if_back_to_2400', 'drawdown','weight']
    # df[['final_asset_if_back_to_2400', 'drawdown']].plot()
    if sum(df['final_asset_if_back_to_2400']*df['weight'])> candidate_val:
        candidate = dict_
        candidate_val = sum(df['final_asset_if_back_to_2400']*df['weight'])
