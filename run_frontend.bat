@echo off
title EduGenie Streamlit Frontend
echo 🧞 Starting EduGenie Streamlit Frontend Dashboard...
echo Dashboard will launch in your browser at http://localhost:8501
"C:\Users\Acer.SNOWYMANAN\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m streamlit run frontend/streamlit_app.py --server.headless=true
pause
