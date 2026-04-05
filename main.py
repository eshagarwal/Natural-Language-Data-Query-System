import subprocess
import os

def main():
    print("Hello!")
    if os.path.exists("venv") or os.path.exists(".venv"):
        subprocess.run(["uv", "run", "streamlit", "run", "app/smartbi.py"])
    else:
        print("Create venv with uv sync then run")
        exit(-1)


if __name__ == "__main__":
    main()
