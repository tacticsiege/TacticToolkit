import os

def get_env_dir():
    ttk_dir = os.path.dirname(os.path.abspath(__file__))
    env_dir = ttk_dir + '\\..\\env\\'
    return env_dir