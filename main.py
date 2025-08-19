from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import json
import os
from datetime import datetime

app = FastAPI()

users_db = []
workouts_db = []
exercises_db = []
progress_db = []
nutrition_db = []
chat_history = []

class User(BaseModel):
    id: int
    username: str
    email: str
    password: str
    age: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    fitness_goals: Optional[str] = None
    medical_conditions: Optional[str] = None
    activity_level: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class Workout(BaseModel):
    id: int
    user_id: int
    plan_name: str
    difficulty_level: str
    duration: int
    target_muscle_groups: str
    exercises_list: str
    date: Optional[str] = None

class Exercise(BaseModel):
    id: int
    exercise_name: str
    category: str
    equipment_needed: str
    difficulty: str
    instructions: str
    target_muscles: str

class Progress(BaseModel):
    id: int
    user_id: int
    workout_id: int
    date: str
    exercises_completed: str
    sets: int
    reps: int
    weights: float
    duration: int
    calories_burned: int

class Nutrition(BaseModel):
    id: int
    user_id: int
    date: str
    meals: str
    calories: int
    protein: float
    carbs: float
    fats: float

class ChatMessage(BaseModel):
    user_id: int
    message: str

def get_next_id(db_list):
    if not db_list:
        return 1
    return max([item.id for item in db_list]) + 1

@app.post("/auth/register")
def register_user(user: User):
    for existing_user in users_db:
        if existing_user.username == user.username:
            raise HTTPException(status_code=400, detail="Username already exists")
    
    user.id = get_next_id(users_db)
    users_db.append(user)
    return {"message": "User registered successfully", "user_id": user.id}

@app.post("/auth/login")
def login_user(login_data: UserLogin):
    for user in users_db:
        if user.username == login_data.username and user.password == login_data.password:
            return {"message": "Login successful", "user_id": user.id, "username": user.username}
    
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/auth/user/{user_id}")
def get_user_profile(user_id: int):
    for user in users_db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.get("/workouts")
def get_workouts(limit: int = 10, offset: int = 0):
    return workouts_db[offset:offset+limit]

@app.post("/workouts")
def create_workout(workout: Workout):
    workout.id = get_next_id(workouts_db)
    workout.date = str(datetime.now().date())
    workouts_db.append(workout)
    return workout

@app.put("/workouts/{workout_id}")
def update_workout(workout_id: int, workout: Workout):
    for i, w in enumerate(workouts_db):
        if w.id == workout_id:
            workout.id = workout_id
            workouts_db[i] = workout
            return workout
    raise HTTPException(status_code=404, detail="Workout not found")

@app.delete("/workouts/{workout_id}")
def delete_workout(workout_id: int):
    for i, w in enumerate(workouts_db):
        if w.id == workout_id:
            del workouts_db[i]
            return {"message": "Workout deleted"}
    raise HTTPException(status_code=404, detail="Workout not found")

@app.get("/exercises")
def get_exercises():
    return exercises_db

@app.post("/exercises")
def create_exercise(exercise: Exercise):
    exercise.id = get_next_id(exercises_db)
    exercises_db.append(exercise)
    return exercise

@app.put("/exercises/{exercise_id}")
def update_exercise(exercise_id: int, exercise: Exercise):
    for i, e in enumerate(exercises_db):
        if e.id == exercise_id:
            exercise.id = exercise_id
            exercises_db[i] = exercise
            return exercise
    raise HTTPException(status_code=404, detail="Exercise not found")

@app.delete("/exercises/{exercise_id}")
def delete_exercise(exercise_id: int):
    for i, e in enumerate(exercises_db):
        if e.id == exercise_id:
            del exercises_db[i]
            return {"message": "Exercise deleted"}
    raise HTTPException(status_code=404, detail="Exercise not found")

@app.get("/progress")
def get_progress():
    return progress_db

@app.post("/progress")
def create_progress(progress: Progress):
    progress.id = get_next_id(progress_db)
    progress_db.append(progress)
    return progress

@app.put("/progress/{progress_id}")
def update_progress(progress_id: int, progress: Progress):
    for i, p in enumerate(progress_db):
        if p.id == progress_id:
            progress.id = progress_id
            progress_db[i] = progress
            return progress
    raise HTTPException(status_code=404, detail="Progress not found")

@app.delete("/progress/{progress_id}")
def delete_progress(progress_id: int):
    for i, p in enumerate(progress_db):
        if p.id == progress_id:
            del progress_db[i]
            return {"message": "Progress deleted"}
    raise HTTPException(status_code=404, detail="Progress not found")

@app.get("/nutrition")
def get_nutrition():
    return nutrition_db

@app.post("/nutrition")
def create_nutrition(nutrition: Nutrition):
    nutrition.id = get_next_id(nutrition_db)
    nutrition_db.append(nutrition)
    return nutrition

@app.put("/nutrition/{nutrition_id}")
def update_nutrition(nutrition_id: int, nutrition: Nutrition):
    for i, n in enumerate(nutrition_db):
        if n.id == nutrition_id:
            nutrition.id = nutrition_id
            nutrition_db[i] = nutrition
            return nutrition
    raise HTTPException(status_code=404, detail="Nutrition not found")

@app.delete("/nutrition/{nutrition_id}")
def delete_nutrition(nutrition_id: int):
    for i, n in enumerate(nutrition_db):
        if n.id == nutrition_id:
            del nutrition_db[i]
            return {"message": "Nutrition deleted"}
    raise HTTPException(status_code=404, detail="Nutrition not found")

@app.post("/chat/ask")
def ask_question(chat_message: ChatMessage):
    try:
        from rag import ask_fitness_question
        
        response = ask_fitness_question(chat_message.message)
        
        chat_entry = {
            "user_id": chat_message.user_id,
            "question": chat_message.message,
            "response": response,
            "timestamp": str(datetime.now())
        }
        chat_history.append(chat_entry)
        
        return {"response": response}
    except Exception as e:
        response = f"I'm having trouble accessing my knowledge base right now. Here's a general response: Thank you for asking '{chat_message.message}'. Please make sure you're asking about fitness, nutrition, or exercises."
        
        chat_entry = {
            "user_id": chat_message.user_id,
            "question": chat_message.message,
            "response": response,
            "timestamp": str(datetime.now())
        }
        chat_history.append(chat_entry)
        
        return {"response": response}

@app.get("/chat/history/{user_id}")
def get_chat_history(user_id: int):
    user_chats = []
    for chat in chat_history:
        if chat["user_id"] == user_id:
            user_chats.append(chat)
    return user_chats

def load_sample_data():
    sample_user = User(
        id=1,
        username="john_doe",
        email="john@example.com",
        password="password123",
        age=25,
        weight=70.0,
        height=175.0,
        fitness_goals="Weight loss",
        activity_level="Beginner"
    )
    users_db.append(sample_user)
    
    sample_exercise = Exercise(
        id=1,
        exercise_name="Push-ups",
        category="Strength",
        equipment_needed="None",
        difficulty="Beginner",
        instructions="Start in plank position, lower body to ground, push back up",
        target_muscles="Chest, Arms"
    )
    exercises_db.append(sample_exercise)

load_sample_data()

