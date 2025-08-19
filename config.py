import os

API_HOST = "localhost"
API_PORT = 8000
DEBUG_MODE = True

DATABASE_URL = "sqlite:///smartfit.db"

OPENAI_MODEL = "gpt-3.5-turbo"
OPENAI_MAX_TOKENS = 300
OPENAI_TEMPERATURE = 0.7

CHROMA_COLLECTION_NAME = "fitness_knowledge"
CHROMA_PERSIST_DIRECTORY = "./chroma_db"

APP_NAME = "SmartFit"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "AI-Powered Fitness Coach"

DEFAULT_EXERCISES = [
    "Push-ups",
    "Squats", 
    "Plank",
    "Jumping Jacks",
    "Lunges"
]

DIFFICULTY_LEVELS = ["Beginner", "Intermediate", "Advanced"]
EXERCISE_CATEGORIES = ["Strength", "Cardio", "Flexibility", "Balance"]

DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100

DATA_FOLDER = "data"
LOGS_FOLDER = "logs"
BACKUP_FOLDER = "backups"

ENABLE_CHAT = True
ENABLE_WORKOUTS = True
ENABLE_NUTRITION = True
ENABLE_PROGRESS = True
