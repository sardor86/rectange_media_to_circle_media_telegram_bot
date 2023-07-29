from environs import Env
from pathlib import Path


env = Env()
env.read_env('.env')

TOKEN = env.str('TOKEN')

path = str(Path(__file__).parent)

