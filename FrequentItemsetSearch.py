import os
import pandas as pd
import numpy as np
import time
import tracemalloc
import matplotlib.pyplot as plt

PATH = 'E:\\本科课程汇总\\本科实验课程\\大数据原理\\LAB5'
INPUT_FILE = 'Groceries.csv'
THRESHOLD = 5

def Construct(distribution, distribution_k, k, threshold):
    """
    Construct distribution_kplus1
    Construct L_k+1 using L_1 and L_k

    Args:
        distribution (dict): A dictionary recording the distribution of frequent items.
        distribution_k (dict): A dictionary recording the distribution of frequent k-itemsets.
        k (int): Current k.
        threshold (int): Support threshold.

    Returns:
        Void (The results will be written to files)
    """

    L1 = list(distribution.keys())
    Lk = list(distribution_k.keys())
    distribution_kplus1 = {}

    for itemset in Lk:
        for item in L1:
            if itemset[-1] < item[0]:               # 保证结果不重复且生成的 itemset 有序
                Tset = distribution_k[itemset] & distribution[item]     # 取交集, 两者同时出现的事务集合
                if len(Tset) >= threshold:          # 判断在事务中出现的次数是否大于 threshold 
                    temp = list(itemset).copy()
                    temp.append(item[0])
                    distribution_kplus1[tuple(temp)] = Tset
    
    return distribution_kplus1

def FrequentItemsetSearch(T, threshold):
    """
    Search frequent Itemset

    Args:
        T (2D - list): 2D transaction list.
        threshold (int): Support threshold.

    Returns:
        Void (The results will be written to files)
    """

    k = 1

    execution_times = []
    items = set()                       # item 集合
    for t in T:
        for item in t:
            items.add(item)

    distribution = dict()               # 记录 frequent item 分布的字典(frequent item : corresponding transaction set)

    print('Computing L1...')
    start_time = time.time()
    for item in items:
        Tset = set()
        temp = []
            
        for tid, t in enumerate(T):     # 遍历事务集
            if item in t:               # item 是否在某一事务中出现
                Tset.add(tid)
        
        if len(Tset) >= threshold:      # 若 item 在事务中的出现次数大于 threshold, 则将其加入 distribution
            temp.append(item)
            distribution[tuple(temp)] = Tset
        
    end_time = time.time()
    
    print(f'Computing L1 spent {end_time - start_time} s.')
    print(f'The number of L1 = {len(distribution)}.')
    print('Writing L1...\n')
    with open(f'result//threshold={threshold}//L1.txt', 'w') as file:
        for item in distribution.keys():
                file.write(', '.join(item) + '\n')

    execution_times.append(end_time - start_time)
    distribution_k = distribution
    
    while(distribution_k):

        print(f'Constructing L{k+1}...')
        start_time = time.time()
        distribution_kpuls1 = Construct(distribution, distribution_k, k, threshold)     # 利用 L_1 和 L_k 构建 L_k+1
        end_time = time.time()
        print(f'Constructing L{k+1} spent {(end_time - start_time):.4f} s.')

        print(f'The number of L{k+1} = {len(distribution_kpuls1)}.')

        if distribution_kpuls1:
            print(f'Writing L{k+1}...\n')
            with open(f'result//threshold={threshold}//L{k+1}.txt', 'w') as file:
                for itemset in distribution_kpuls1.keys():
                    file.write(', '.join(itemset) + '\n')

        execution_times.append(end_time - start_time)
        distribution_k = distribution_kpuls1
        k = k + 1

    return execution_times

if __name__ == '__main__':
    
    if not os.path.exists(os.path.join(PATH, f'result//threshold={THRESHOLD}')):
        os.makedirs(os.path.join(PATH, f'result//threshold={THRESHOLD}'))
    
    os.chdir(PATH)

    # 开始跟踪内存分配
    # tracemalloc.start()

    # 读取事务数据集
    data = pd.read_csv(INPUT_FILE)
    data = np.array(data['items'])

    # 用来存储事务的列表
    T = []  
    for d in data:
        T.append(d.replace("{", "").replace("}", "").split(','))
    
    start_time = time.time()
    execution_times = FrequentItemsetSearch(T, THRESHOLD)
    end_time = time.time()

    print(f'Total time = {(end_time - start_time):.4f} s.')
    
    # 获取当前内存使用和峰值内存使用
    # current, peak = tracemalloc.get_traced_memory()
    # print(f"Peak memory usage: {peak / 10**6 :.4f} MB.\n")

    # 停止跟踪内存分配
    tracemalloc.stop()

    print('Normal end of execution.\n')

    # 绘制柱状图
    plt.figure(figsize=(10, 6))
    plt.bar(range(1, len(execution_times) + 1), execution_times, color='orange')
    plt.xlabel('Iteration (k)')
    plt.ylabel('Time (seconds)')
    plt.title('Execution Time per Iteration')
    plt.xticks(range(1, len(execution_times) + 1))
    plt.grid(axis='y')
    plt.show()
