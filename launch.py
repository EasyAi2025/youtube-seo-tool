
import os
import webbrowser
import threading

def open_browser():
    webbrowser.open_new("http://localhost:8501?fullscreen=true")

threading.Timer(1.5, open_browser).start()
os.system("streamlit run my_vidiq_combined.py")
