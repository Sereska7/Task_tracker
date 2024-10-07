import os
from dotenv import load_dotenv

os.environ["MODE"] = "TEST"

load_dotenv('.env')
