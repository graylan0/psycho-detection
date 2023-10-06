import re
import openai
import pennylane as qml
from pennylane import numpy as np
import asyncio
import json
import nest_asyncio
import aiosqlite
import speech_recognition as sr
import threading
import time
from textblob import TextBlob

# Load configuration from JSON
with open("config.json", "r") as f:
    config = json.load(f)

openai.api_key = config["openai_api_key"]
nest_asyncio.apply()

# Initialize Quantum Language Model
qml_model = qml.device('default.qubit', wires=4)

async def create_table():
    async with aiosqlite.connect("emotional_data.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS emotional_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                emotion TEXT,
                color_code TEXT,
                quantum_state TEXT,
                amplitude REAL,
                cluster_label TEXT,
                cluster_color_code TEXT,
                psychosis_detection_state TEXT
            );
        """)
        await db.commit()

async def store_emotional_data(emotion, color_code, quantum_state, amplitude, cluster_label, cluster_color_code, psychosis_detection_state):
    async with aiosqlite.connect("emotional_data.db") as db:
        await db.execute("""
            INSERT INTO emotional_data (emotion, color_code, quantum_state, amplitude, cluster_label, cluster_color_code, psychosis_detection_state)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (emotion, color_code, str(quantum_state.tolist()), amplitude, cluster_label, cluster_color_code, psychosis_detection_state))
        await db.commit()

def sentiment_to_amplitude(text):
    analysis = TextBlob(text)
    return (analysis.sentiment.polarity + 1) / 2

@qml.qnode(qml_model)
def quantum_circuit(color_code, amplitude):
    r, g, b = [int(color_code[i:i+2], 16) for i in (1, 3, 5)]
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    qml.RY(r * np.pi, wires=0)
    qml.RY(g * np.pi, wires=1)
    qml.RY(b * np.pi, wires=2)
    qml.RY(amplitude * np.pi, wires=3)
    qml.CNOT(wires=[0, 1])
    qml.CNOT(wires=[1, 2])
    qml.CNOT(wires=[2, 3])
    return qml.state()

async def record_emotion():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Please wait. Calibrating microphone...")
        recognizer.adjust_for_ambient_noise(source, duration=5)
        print("Microphone calibrated.")
        print("Recording for 15 seconds...")
        audio_data = recognizer.listen(source, timeout=15)
        print("Recording complete.")

    return recognizer.recognize_google(audio_data)

async def generate_emotion_data(emotion, task1_label, task2_label, task3_label):
    try:
        # Task 1: Generate HTML color code
        task1_prompt = f"Please generate an HTML color code that best represents the emotion: {emotion}."
        task1_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": task1_prompt}
            ]
        )
        color_code = re.search(r'#[0-9a-fA-F]{6}', task1_response['choices'][0]['message']['content'])
        
        amplitude = None  # Initialize amplitude
        
        if color_code:
            # Calculate amplitude if color code is available
            amplitude = sentiment_to_amplitude(emotion)
        
        # Task 3: Generate quantum state
        if color_code:
            quantum_state = quantum_circuit(color_code.group(0), amplitude).numpy()
        else:
            quantum_state = None

        # Store the data
        await store_emotional_data(emotion, color_code.group(0) if color_code else None, quantum_state, amplitude, task1_label, task2_label, None)  # Removed task3_label

        # Task 2: Perform psychosis detection using ChatGPT with quantum data
        task2_prompt = f"Please analyze the user's input as {quantum_state} this is the {amplitude} and the text generating the quantum state: {emotion}, and provide insights into psychosis detection by providing the following 1. Only reply with Yes or No as the first words, after yes or no, then the clusting of emotions and potential if any of mania or depression or psychosis  Following is  quantum state data that provides a right to left emotional and brain capacitive delivery of understanding to ai models. Interpreate the data from the text in the example. DO your best as a model who must follow the guideance. and provide Yes or No{quantum_state}."
        task2_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant.DO your best as a model who must follow the guideance. and provide Yes or No"},
                {"role": "user", "content": task2_prompt}
            ]
        )
        psychosis_detection_state = task2_response['choices'][0]['message']['content']

        # Update the stored data with psychosis detection information
        await update_psychosis_detection_state(emotion, psychosis_detection_state)

    except openai.error.InvalidRequestError as e:
        print(f"OpenAI error: {e}")

async def update_psychosis_detection_state(emotion, psychosis_detection_state):
    async with aiosqlite.connect("emotional_data.db") as db:
        await db.execute("""
            UPDATE emotional_data
            SET psychosis_detection_state = ?
            WHERE emotion = ?
        """, (psychosis_detection_state, emotion))
        await db.commit()

async def main():
    await create_table()
    emotion = await record_emotion()
    
    # Create a thread to run the coroutine
    thread = threading.Thread(target=lambda: asyncio.run(generate_emotion_data(emotion, "color_code", "psychosis_detection_state", "quantum_state")))
    thread.start()
    
if __name__ == "__main__":
    asyncio.run(main())
