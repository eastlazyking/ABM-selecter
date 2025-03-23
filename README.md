# 介紹
這是一個使用 `tkinter` 製作的簡易 GUI 工具，目的是讓你可以透過視覺介面選擇 `.py` 檔案並直接執行它。適合用來快速測試小型 Python 程式，不必每次都打開終端機。

# 資料夾架構
abm-selecter/
├── app.py                      # tkinter GUI 主程式
├── scripts/                     # 存放 .py 檔案
├── output/                    # 存放 .py 的圖片結果
├── Dockerfile
├── requirements.txt    # Docker所需的pip模組列表
└── README.md
└── Start.bat                   # 執行

# 執行步驟
1. 確保已經執行 Start.bat，python_runner container 正在跑
2. 確保 scripts/ 資料夾中有 .py 檔案可以執行
3. 執行 app.py
4. 選一個 .py，點「執行檔案」，看結果是否印在畫面上 

# 開發進度紀錄
## 20250324
+ GUI 可以選擇並執行 .py 模型
+ 模型會自動儲存圖片，以台灣時間戳記檔名，避免Docker預設時間是UTC的時區問題
+ 執行完後自動打開最新圖片
+ Docker container 正常跑，不會閃退，用 tail -f /dev/null 保持存活
+ subprocess 中文輸出解決編碼錯誤，改為 encoding="utf-8"

# 下次要幹嘛
 GUI加參數欄位：讓使用者輸入 agent 數量、模擬秒數，把輸入的參數「當作指令列參數」傳進 .py 模型