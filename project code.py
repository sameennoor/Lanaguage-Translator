# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 21:02:43 2024

@author: Dell
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 20:36:20 2024

@author: Dell
"""

import tkinter as tk
from tkinter import messagebox, ttk
import threading
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os

# Initialize the translator and recognizer
translator = Translator()
recognizer = sr.Recognizer()
audio_data = None
is_listening = False  # Tracks whether listening is in progress

# Language and accent mappings
language_mapping = {
    "Persian": "fa",
    "Arabic": "ar",
    "English": "en",
    "Spanish": "es",
    "Korean": "ko",
    "Chinese": "zh-cn",
    "German": "de",
    "Russian": "ru",
    "Italian": "it",
    "French": "fr",
    "Urdu": "ur"
}

# Function to start listening
def start_listening():
    global audio_data, is_listening
    result_text.set("Listening...")
    root.update()

    try:
        with sr.Microphone() as source:
            recognizer.energy_threshold = 500
            recognizer.dynamic_energy_threshold = False
            recognizer.pause_threshold = 0.8
            is_listening = True
            audio_data = recognizer.listen(source, timeout=10, phrase_time_limit=6)
            result_text.set("Listening complete. Ready for translation.")
            is_listening = False
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while listening: {e}")
        is_listening = False

# Function to process translation
def process_translation():
    global audio_data
    if audio_data is None:
        result_text.set("No audio data captured. Please try again.")
        return

    input_language = input_language_var.get()
    target_language = target_language_var.get()

    if input_language not in language_mapping or target_language not in language_mapping:
        messagebox.showerror("Error", "Please select valid input and target languages.")
        return

    source_language_code = language_mapping[input_language]
    target_language_code = language_mapping[target_language]

    try:
        # Recognize speech
        result_text.set("Processing translation...")
        text = recognizer.recognize_google(audio_data, language=source_language_code)
        original_text.set(f"Original Text: {text}")

        # Translate recognized text
        translated = translator.translate(text, src=source_language_code, dest=target_language_code)
        translated_text.set(f"Translated Text: {translated.text}")

        # Use gTTS to generate audio for translation
        tts = gTTS(translated.text, lang=target_language_code)
        tts.save("translated_speech.mp3")

        if os.name == 'nt':
            os.system("start translated_speech.mp3")
        elif os.name == 'posix':
            os.system("open translated_speech.mp3")

        result_text.set(f"Translation complete to {target_language}.")

    except sr.UnknownValueError:
        messagebox.showerror("Error", "Could not understand the audio")
    except sr.RequestError as e:
        messagebox.showerror("Error", f"Could not request results; {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to handle the Start button
def on_start_button_click():
    if not is_listening:
        threading.Thread(target=start_listening).start()
    else:
        result_text.set("Already listening. Please stop before restarting.")

# Function to handle the Stop button
def on_stop_button_click():
    if is_listening:
        result_text.set("Processing translation...")
        threading.Thread(target=process_translation).start()
    else:
        result_text.set("No listening in progress to stop.")

# Setting up the GUI
root = tk.Tk()
root.title("Language Translator")
root.geometry("600x700")
root.configure(bg="#f0f5ff")  # Light blue background

# Styling
header_font = ("Helvetica", 18, "bold")
subheader_font = ("Helvetica", 12)
button_font = ("Helvetica", 14, "bold")
text_font = ("Helvetica", 12)
text_color = "#333333"
bg_color = "#f0f5ff"  # Light blue
accent_color = "#003366"  # Royal blue
button_color = "#003366"
button_hover_color = "#002244"
label_bg = "#ffffff"
label_fg = "#333333"

# Header
header_frame = tk.Frame(root, bg=accent_color, pady=15)
header_frame.pack(fill="x")
header_label = tk.Label(header_frame, text="Language Translator", font=header_font, fg="white", bg=accent_color)
header_label.pack()

# Instructions
instruction_frame = tk.Frame(root, bg=bg_color, pady=15)
instruction_frame.pack(fill="x")
instruction_label = tk.Label(instruction_frame, text="Select input and target languages, click 'Start' to listen, then 'Stop' to translate.", font=subheader_font, bg=bg_color, fg=text_color)
instruction_label.pack()

# Dropdowns for language selection
dropdown_frame = tk.Frame(root, bg=bg_color, pady=10)
dropdown_frame.pack(fill="x")

# Input Language
input_language_var = tk.StringVar()
input_language_var.set("English")
input_language_label = tk.Label(dropdown_frame, text="Input Language:", font=text_font, bg=bg_color, fg=text_color)
input_language_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
input_language_dropdown = ttk.Combobox(dropdown_frame, textvariable=input_language_var, values=list(language_mapping.keys()), font=text_font, width=20)
input_language_dropdown.grid(row=0, column=1, pady=5)

# Target Language
target_language_var = tk.StringVar()
target_language_var.set("Urdu")
target_language_label = tk.Label(dropdown_frame, text="Target Language:", font=text_font, bg=bg_color, fg=text_color)
target_language_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
target_language_dropdown = ttk.Combobox(dropdown_frame, textvariable=target_language_var, values=list(language_mapping.keys()), font=text_font, width=20)
target_language_dropdown.grid(row=1, column=1, pady=5)

# Start and Stop Buttons
button_frame = tk.Frame(root, bg=bg_color, pady=15)
button_frame.pack(fill="x")
start_button = tk.Button(button_frame, text="Start Listening", font=button_font, bg=button_color, fg="white", relief="solid", command=on_start_button_click)
start_button.grid(row=0, column=0, padx=10, pady=5)
stop_button = tk.Button(button_frame, text="Stop & Translate", font=button_font, bg=button_color, fg="white", relief="solid", command=on_stop_button_click)
stop_button.grid(row=0, column=1, padx=10, pady=5)

# Result Text Display
text_frame = tk.Frame(root, bg=bg_color, pady=15)
text_frame.pack(fill="x")
original_text = tk.StringVar()
translated_text = tk.StringVar()
result_text = tk.StringVar()

original_label = tk.Label(text_frame, textvariable=original_text, wraplength=500, font=text_font, bg=label_bg, fg=label_fg, relief="solid")
original_label.pack(pady=5)
translated_label = tk.Label(text_frame, textvariable=translated_text, wraplength=500, font=text_font, bg=label_bg, fg="green", relief="solid")
translated_label.pack(pady=5)
result_label = tk.Label(text_frame, textvariable=result_text, font=("Helvetica", 12, "italic"), bg=bg_color, fg=text_color)
result_label.pack(pady=5)

# Run the GUI loop
root.mainloop()
