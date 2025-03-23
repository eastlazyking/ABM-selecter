@echo off

REM ✅ 只在 image 不存在時才 build（image = 執行環境的模型）
docker image inspect abm-docker >nul 2>&1 || docker build -t abm-docker .

REM ❌ 移除之前可能殘留的 container（container = 跑起來的實例）
docker rm -f python_runner >nul 2>&1

REM 🚀 啟動新的 container，掛載 scripts 和 output 資料夾，使用 abm-docker image
docker run -dit ^
  --name python_runner ^
  -v "%cd%\scripts:/app/scripts" ^
  -v "%cd%\output:/app/output" ^
  abm-docker ^
  tail -f /dev/null

REM 🐍 執行你的 GUI（app.py）
echo start GUI
python app.py

pause
