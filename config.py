from dotenv.main import load_dotenv
from pathlib import Path
import os


load_dotenv()
TOKEN = os.environ['TOKEN']

path = str(Path(__file__).parent)

