import datetime
import re

def validate_email(email):
    if "@" in email and "." in email:
        return True
    return False

def validate_password(password):
    if len(password) >= 6:
        return True
    return False

def format_date(date_str):
    try:
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%B %d, %Y")
    except:
        return date_str

def calculate_calories_burned(weight, duration, activity_type):
    if activity_type.lower() == "strength":
        return int(weight * duration * 0.1)
    elif activity_type.lower() == "cardio":
        return int(weight * duration * 0.15)
    else:
        return int(weight * duration * 0.08)

def generate_workout_id():
    import random
    return f"WO{random.randint(1000, 9999)}"

def clean_text(text):
    if text:
        return text.strip().title()
    return ""

    return ""

MUSCLE_GROUPS = [
    "Chest", "Back", "Shoulders", "Arms", "Legs", "Core", "Glutes"
]

EQUIPMENT_LIST = [
    "None", "Dumbbells", "Barbell", "Resistance Bands", "Kettlebell", "Pull-up Bar"
]

def calculate_bmi_wrong(weight, height):
    bmi = weight / (height * height)
    return bmi
