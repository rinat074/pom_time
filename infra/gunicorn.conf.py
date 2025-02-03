from dotenv import load_dotenv
from uvicorn.workers import UvicornWorker
import os

bind = "0.0.0.0:8000"
workers = 4

enviroment = os.getenv("ENVIROMENT") #export ENVIROMENT=local

env = os.path.join(os.getcwd(), f".{enviroment}.env")

if os.path.exists(env):
    print(f"Loading environment from {env}")
    load_dotenv(env)
else:
    print(f"Environment file {env} not found")
