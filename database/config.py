from dotenv import load_dotenv
import os

load_dotenv()

mysql_path = os.getenv("MYSQL_PATH")
secret_key = os.getenv("SECRET_KEY")
