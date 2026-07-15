@echo off
title EduGenie FastAPI Backend
echo 🧞 Starting EduGenie FastAPI Backend Server...
echo API docs will be available at http://127.0.0.1:8000/docs
"C:\Users\Acer.SNOWYMANAN\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m uvicorn app.main:app --reload --port 8000
pause
