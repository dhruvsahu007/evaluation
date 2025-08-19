import chromadb
from chromadb.utils import embedding_functions
import openai
import os
from typing import List

client = chromadb.Client()

try:
    collection = client.get_collection("fitness_knowledge")
except:
    collection = client.create_collection("fitness_knowledge")

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY", "your-api-key-here"),
    model_name="text-embedding-ada-002"
)

fitness_knowledge = [
    {
        "id": "ex1",
        "content": "Push-ups are a fundamental bodyweight exercise that targets the chest, shoulders, and triceps. To perform a push-up: Start in a plank position with hands shoulder-width apart. Lower your body until your chest nearly touches the floor. Push back up to starting position. Keep your core tight throughout the movement.",
        "category": "exercise",
        "metadata": {"exercise_type": "bodyweight", "difficulty": "beginner"}
    },
    {
        "id": "ex2", 
        "content": "Squats are a compound exercise that primarily targets the quadriceps, hamstrings, and glutes. To perform a squat: Stand with feet shoulder-width apart. Lower your body as if sitting back into a chair. Keep your chest up and knees behind your toes. Push through your heels to return to starting position.",
        "category": "exercise",
        "metadata": {"exercise_type": "bodyweight", "difficulty": "beginner"}
    },
    {
        "id": "ex3",
        "content": "Deadlifts are one of the most effective exercises for building overall strength. They target the hamstrings, glutes, lower back, and core. Always maintain proper form: Keep your back straight, chest up, and lift with your legs. Start with lighter weights and progress gradually.",
        "category": "exercise", 
        "metadata": {"exercise_type": "weighted", "difficulty": "intermediate"}
    },
    {
        "id": "nut1",
        "content": "Protein is essential for muscle building and recovery. Aim for 0.8-1.2 grams of protein per kilogram of body weight. Good sources include chicken, fish, eggs, beans, and nuts. Consume protein throughout the day, especially after workouts.",
        "category": "nutrition",
        "metadata": {"topic": "macronutrients"}
    },
    {
        "id": "nut2",
        "content": "Carbohydrates provide energy for workouts. Complex carbs like oats, brown rice, and sweet potatoes are better than simple sugars. Time your carb intake around workouts for optimal performance and recovery.",
        "category": "nutrition",
        "metadata": {"topic": "macronutrients"}
    },
    {
        "id": "fit1",
        "content": "Progressive overload is the key principle for building strength and muscle. Gradually increase weight, reps, or sets over time. Track your workouts to ensure you're progressing. Rest is also important - allow 48-72 hours between training the same muscle groups.",
        "category": "fitness_principles",
        "metadata": {"topic": "training"}
    },
    {
        "id": "fit2",
        "content": "Recovery is just as important as training. Get 7-9 hours of sleep per night. Stay hydrated by drinking plenty of water. Include rest days in your routine. Listen to your body and don't train through pain.",
        "category": "fitness_principles",
        "metadata": {"topic": "recovery"}
    }
]

def initialize_knowledge_base():
    try:
        if collection.count() > 0:
            print("Knowledge base already initialized")
            return
        
        documents = [item["content"] for item in fitness_knowledge]
        ids = [item["id"] for item in fitness_knowledge]
        metadatas = [{"category": item["category"], **item["metadata"]} for item in fitness_knowledge]
        
        collection.add(
            documents=documents,
            ids=ids,
            metadatas=metadatas
        )
        print(f"Added {len(documents)} documents to knowledge base")
    except Exception as e:
        print(f"Error initializing knowledge base: {e}")

def search_knowledge(query: str, n_results: int = 3):
    try:
        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results
    except Exception as e:
        print(f"Error searching knowledge base: {e}")
        return None

def generate_response(query: str, context: str):
    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        prompt = f"""You are a helpful fitness coach. Use the following context to answer the user's question about fitness, nutrition, or exercise.

Context:
{context}

User Question: {query}

Please provide a helpful, accurate response based on the context provided. If the context doesn't contain enough information, say so and provide general guidance."""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a knowledgeable fitness coach who provides helpful advice about exercise, nutrition, and fitness."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating response: {e}")
        return "Sorry, I'm having trouble generating a response right now. Please try again later."

def ask_fitness_question(question: str):
    search_results = search_knowledge(question)
    
    if not search_results or not search_results['documents'][0]:
        return "I don't have enough information to answer that question. Please ask about exercises, nutrition, or fitness principles."
    
    context = "\n\n".join(search_results['documents'][0])
    
    response = generate_response(question, context)
    
    return response

initialize_knowledge_base()

def test_rag_system():
    test_questions = [
        "How do I do push-ups correctly?",
        "What should I eat for muscle building?",
        "How important is rest in fitness?"
    ]
    
    for question in test_questions:
        print(f"\nQ: {question}")
        answer = ask_fitness_question(question)
        print(f"A: {answer}")

if __name__ == "__main__":
    test_rag_system()



