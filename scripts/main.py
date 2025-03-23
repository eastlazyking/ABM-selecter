import os
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# 調整Python的工作目錄
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# 讀取土地資訊
land_data = pd.read_csv("Data_Land.csv")
available_land_ids = land_data["id"].tolist()  # 取得 id 列表
selected_land_ids = np.random.choice(available_land_ids, size=50, replace=False) # 隨機選擇 50 個不重複的土地ID
land_sea_level = land_data["sea_level"].tolist()


# 代理人
class Resident: 
    def __init__(self, unique_id, model, age, savings, land_id):
        self.unique_id = unique_id #id
        self.model = model
        self.age = age # 年齡
        self.savings = savings # 存款
        self.land_id = land_id  # 抽到的居住土地的 ID
        self.flooded_count = 0  # x_4: 被水淹次數
        self.awakened = False  # 是否覺醒



    # 計算效用函數
    def utility(self):
        # neighbors_awakened = sum(1 for n in self.model.schedule.agents if n.awakened) #周邊鄰居覺醒人數
        neighbors_awakened = 4
        y = 0.3 * self.age + 0.4 * self.savings + 0.2 * neighbors_awakened + 0.1 * self.flooded_count
        return y
    
    # 模擬一個周期
    def step(self):
        flood_level = np.random.randint(0, 101)  # 101 是因為 randint(a, b) 介於 a ~ b-1

        # 取得該居民所在土地的 sea_level
        land_sea_level = self.model.land_data.loc[self.model.land_data["id"] == self.land_id, "sea_level"].values[0]

        # 判斷是否被水淹
        if land_sea_level < flood_level:
            self.flooded_count += 1

        # 計算效用函數
        utility_value = self.utility()
        if utility_value >= 50:
            self.awakened = True
        else:
            self.awakened = False

        # 儲存
        self.model.utility_values.append(utility_value)

        # 連續10回合未被淹沒 可能覺醒度下降
        if self.flooded_count == 0 and np.random.rand() < 0.3:
            self.awakened = False

# 隨機抽一個
class RandomScheduler:
    def __init__(self):
        self.agents = {}  # 存代理人的字典 {unique_id: agent}

    def add(self, agent):
        """新增代理人到調度器"""
        self.agents[agent.unique_id] = agent

    def step(self, flood_level):
        """隨機選擇代理人執行 step()"""
        agent_ids = list(self.agents.keys())  # 取得所有 agent 的 ID
        random.shuffle(agent_ids)  # 隨機排列 ID
        
        for agent_id in agent_ids:
            self.agents[agent_id].step()  # 讓該 ID 的 agent 執行 step()

# 政府
class FloodingModel:
    def __init__(self):
        self.schedule = RandomScheduler()
        self.land_data = land_data
        self.flooding_level_min = 0  # 洪水最低範圍
        self.flooding_level_max = 100  # 洪水最大範圍
        self.utility_values = [] # 儲存本回合每個agent的效用結果
        # 儲存
        self.avg_utility_list = []  # 每回合的平均效用
        self.flood_levels = []  # 每回合的洪水等級
        self.awakened_ratios = []  # 每回合的覺醒比例

        # 建立 50 個居民
        for i in range(50):
            age = np.random.randint(20, 85)
            savings = np.random.randint(0, 100)
            land_id = selected_land_ids[i]  # 抽到的居住土地的 ID
            resident = Resident(i, self, age, savings, land_id)
            self.schedule.add(resident)

    #模擬一回合
    def step(self):
        self.flooding_level = np.random.randint(self.flooding_level_min, self.flooding_level_max)

        # 清空上一回合的 utility_values，重新記錄本回合的數據
        self.utility_values = []  
        self.schedule.step(self.flooding_level) 

        # 計算平均效用函數結果
        avg_utility = sum(self.utility_values) / len(self.utility_values)
        
        # 計算覺醒比例
        awakened_count = sum(1 for agent in self.schedule.agents.values() if agent.awakened)
        awakened_ratio = awakened_count / 50

        # 如果超過 10% 覺醒，請願建防洪設施
        if awakened_ratio >= 0.1:
            self.flooding_level_min += 1  # 增加最低洪水範圍

        # 儲存數據結果
        self.avg_utility_list.append(avg_utility)     # 平均效用
        self.flood_levels.append(self.flooding_level) # 洪水等級
        self.awakened_ratios.append(awakened_ratio)   # 覺醒比例

        print(f"平均效用: {avg_utility}\n 洪水等級: {self.flooding_level}\n 覺醒比例: {awakened_ratio:.2%}\n 回合結束")

# 跑模型
model = FloodingModel()
for i in range(20):  # 執行 20 年(回合)
    print(f"--- 第 {i+1} 回合 ---")
    model.step()

# 繪製圖表
plt.figure(figsize=(12, 6)) # 設定畫布大小
plt.style.use("ggplot")  # 設定美術主題

# 繪製 平均效用變化圖
plt.subplot(1, 2, 1) # plt.subplot(rows, cols, index)→整體是1 行 2 列的圖表，這是左邊第一張
plt.plot(model.avg_utility_list, marker='o', linestyle='-', linewidth = 2, color='tan', label='avg_utility')
plt.xlabel("Years") # 模擬年
plt.ylabel("Average Utility") # 平均效用
plt.title("Average utility of residents", fontweight='bold') # 居民的平均效用變化
plt.legend()

# 繪製 洪水高度 vs 覺醒比例
plt.subplot(1, 2, 2) # plt.subplot(rows, cols, index)→整體是1 行 2 列的圖表，這是右邊第二張
plt.plot(model.flood_levels, marker='s', linestyle='-', linewidth = 2, color='turquoise', label='Flood Depth')
plt.plot([r * 100 for r in model.awakened_ratios], marker='^', linestyle='--', linewidth = 2, color='olive', label='Awakening Ratio(%)')
plt.xlabel("Years") # 模擬年
plt.ylabel("Flood Depth") # 洪水高度
plt.title("Flood Depth & Awakening Ratio", fontweight='bold')
plt.legend()

plt.tight_layout()
plt.show()

# 儲存
now = datetime.now() + timedelta(hours=8)  # UTC+8 台灣時間
filename = now.strftime("%Y%m%d_%H%M%S") + ".png"
output_path = f"/app/output/{filename}"
plt.savefig(output_path)



