# app/main.py

import subprocess
import sys
import os

def main():
    # Ruta absoluta del archivo app_streamlit.py
    current_dir = os.path.dirname(os.path.abspath(__file__))
    target_file = os.path.join(current_dir, "app_streamlit.py")

    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", target_file], check=True)
    except subprocess.CalledProcessError as e:
        print("❌ Error al lanzar Streamlit:", e)

if __name__ == "__main__":
    main()
