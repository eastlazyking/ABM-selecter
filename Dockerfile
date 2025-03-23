FROM python:3.13.2

# 建立一個工作目錄
WORKDIR /app

# 把你所有的檔案複製進容器內
COPY . .

# 安裝你在 requirements.txt 裡指定的套件
RUN pip install --no-cache-dir -r requirements.txt

# 預設執行你的 Python 檔案（改成你要的檔名）
CMD ["python", "main.py"]


