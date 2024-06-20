import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
import pyttsx3
from groq import Groq

client = Groq(
    api_key="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"
)

system_prompt = """
You are a helpful, respectful and professional assistant.
the conversation should be shorter.
Your task is to assist a marketing team in getting the budget and providing market strategies according to the budget and the platforms they're running ads on.
The platforms include Google and Meta.
You should consider the budget, the target audience, the goals of the campaign, and the strengths and weaknesses of each platform when providing market strategies.
the content should be optimized and summerized.
make the budget in Indian ruppes.
"""

messages = [
    {
        "role": "system",
        "content": system_prompt,
    }
]

# Initialize the speech recognizer and text-to-speech engine
r = sr.Recognizer()
engine = pyttsx3.init()

def send_message():
    user_message = user_input.get("1.0", "end-1c")
    user_input.delete("1.0", "end")
    messages.append({
        "role": "user",
        "content": user_message,
    })
    chat_log.insert(tk.END, f"You: {user_message}\n")

    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama3-8b-8192",
    )

    assistant_message = chat_completion.choices[0].message.content
    chat_log.insert(tk.END, f"Assistant: {assistant_message}\n")
    messages.append({
        "role": "assistant",
        "content": assistant_message,
    })

    # Use the text-to-speech engine to convert text to speech
    engine.say(assistant_message)
    engine.runAndWait()

def listen_for_message():
    # Use the microphone as the audio source
    with sr.Microphone() as source:
        print("Say something!")
        try:
            audio = r.listen(source, timeout=1)
            # Use the speech recognizer to convert speech to text
            user_message = r.recognize_google(audio)
            print(f"You said: {user_message}")
            user_input.insert(tk.END, user_message)
            send_message()
        except sr.WaitTimeoutError:
            # No speech detected, continue listening
            listen_for_message()
        except sr.UnknownValueError:
            print("Sorry, I didn't understand that.")
        except sr.RequestError:
            print("Sorry, I'm having trouble connecting to the speech recognition service.")

def start_listening():
    # Continuously listen for user input
    while True:
        listen_for_message()

root = tk.Tk()
root.title("Marketing Assistant")

chat_log = scrolledtext.ScrolledText(root, width=50, height=10)
chat_log.pack()

user_input = tk.Text(root, width=50, height=3)
user_input.pack()

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack()

listen_button = tk.Button(root, text="Listen", command=start_listening)
listen_button.pack()

root.mainloop()
