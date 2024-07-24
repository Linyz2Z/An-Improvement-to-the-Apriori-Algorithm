# An Improvement to the Apriori Algorithm
2024春中山大学大数据原理与技术期末项目
FINAL PROJECT FOR BIG DATA PRINCIPLES AND TECHNOLOGIES, SYSU, SPRING 2024

## Author
YuLin Zhou, Jiaqi Zhang

## Abstract
Frequent itemset mining is pivotal in data mining with applications such as market basket analysis. The foundational Apriori algorithm, suffers from performance limitations due to its combinatorial nature. We introduces ReverseApriori that reduces the search space by incorporating an intersection approach, thereby pruning non-promising trans-set at each stage, and significantly improves efficiency and scalability. Extensive experiments on real-world datasets demonstrate that our improved algorithm outperforms traditional methods in terms of time and memory.

## Result
TABLE I: Execution Time Efficiency on Small Dataset (9835)

| Algorithm      | Threshold=3 | Threshold=4 | Threshold=5 |
|----------------|-------------|-------------|-------------|
| Apriori        | 3624 s      | 2897 s      | 2355 s      |
| FPtree         | 3.64 s      | 2.66 s      | 2.49 s      |
| ReverseApriori | 3.79 s      | 2.55 s      | 1.66 s      |

TABLE II: Execution Time Efficiency on Big Dataset (98350)

| Algorithm      | Threshold=3 | Threshold=4 | Threshold=5 |
|----------------|-------------|-------------|-------------|
| Apriori        | >1 day      | >1 day      | >1 day      |
| FPtree         | 26.82 s     | 24.79 s     | 27.62 s     |
| ReverseApriori | 18.82 s     | 14.10 s     | 13.33 s     |
