import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные из .env
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

