import tkinter as tk                        # 建立 GUI 視窗
from tkinter import filedialog, messagebox  # 檔案選擇視窗、訊息彈出視窗
import subprocess                           # 執行終端機指令
import os                                   # 處理檔案路徑（主機路徑）
import glob
import time

CONTAINER_NAME = "python_runner" # Docker container的名字 與Dockerfile連動
SCRIPTS_DIR_NAME = "scripts"     # 放py的地方

# 去放py的地方找py檔
def select_file():
    filepath = filedialog.askopenfilename(
        initialdir=os.path.join(os.getcwd(), SCRIPTS_DIR_NAME),
        filetypes=[("Python files", "*.py")]
    )
    if filepath:
        selected_file.set(filepath)

# 把主機路徑轉換成 container 路徑
def convert_to_container_path(host_path):
    filename = os.path.basename(host_path) # 主機路徑
    return f"/app/scripts/{filename}"      # container路徑 /app/scripts/與Dockerfile連動

# 在 Docker container 裡執行 py 檔
def run_script():
    host_path = selected_file.get()
    if not host_path:
        messagebox.showwarning("提醒", "請先選擇一個 .py 檔案")
        return

    container_path = convert_to_container_path(host_path)

    try:
        result = subprocess.run(
            ["docker", "exec", CONTAINER_NAME, "python", container_path],
            capture_output=True, text=True, encoding="utf-8"
        )
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"🟢 執行結果：\n{result.stdout}\n")
        if result.stderr:
            output_text.insert(tk.END, f"🔴 錯誤訊息：\n{result.stderr}")

        # 自動打開最新的圖片結果
        output_folder = os.path.join(os.getcwd(), "output")
        image_files = glob.glob(os.path.join(output_folder, "*.png"))

        if image_files:
            # 按照最後修改時間排序，取最新的一張
            latest_image = max(image_files, key=os.path.getmtime)
            os.startfile(latest_image)
        else:
            output_text.insert(tk.END, "⚠️ 沒有找到任何圖片，請確認模型有產圖\n")
    
    except Exception as e:
        messagebox.showerror("錯誤", f"執行失敗：{e}")

# 建立 GUI 視窗
root = tk.Tk()
root.title("🐍 ABM selecter")
root.geometry("600x400")

selected_file = tk.StringVar()  # 用來儲存你選的檔案路徑

tk.Button(root, text="選擇 Python 檔", command=select_file).pack(pady=10)
tk.Label(root, textvariable=selected_file, wraplength=580).pack(pady=5)
tk.Button(root, text="執行檔案", command=run_script).pack(pady=10)

output_text = tk.Text(root, height=15, wrap=tk.WORD)
output_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

root.mainloop()
