import os

from dotenv import load_dotenv

load_dotenv()


HF_TOKEN = os.getenv("HF_TOKEN")

HF_MODEL = os.getenv(
    "HF_MODEL",
    "Qwen/Qwen3-4B-Instruct-2507",
)


MONGO_URI = os.getenv("MONGO_URI")

MONGO_DB_NAME = os.getenv(
    "MONGO_DB_NAME",
    "studymate",
)


CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173",
    ).split(",")
    if origin.strip()
]


DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
)

os.makedirs(DATA_DIR, exist_ok=True)


if not HF_TOKEN:
    print("WARNING: HF_TOKEN is not configured.")

if not MONGO_URI:
    print("WARNING: MONGO_URI is not configured.")