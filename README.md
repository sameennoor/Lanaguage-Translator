# AI Based Language Translator App
## Project Overview
The AI-Based Language Translator is a Python desktop application that enables real-time translation of spoken language into another language. It combines speech recognition, language translation, and text-to-speech to create a seamless communication experience.
## Features

🎤 Speech-to-text conversion using Google Speech Recognition.

🌍 Real-time multilingual translation via Google Translate.

🔊 Text-to-speech playback using gTTS.

🖥️ User-friendly GUI built with Tkinter.

⚠️ Smart error handling for speech, translation, and audio issues.

## Technologies Used

Language: Python

Libraries: Tkinter, SpeechRecognition, GoogleTrans, gTTS, os

APIs: Google Speech Recognition, Google Translate, Google Text-to-Speech

## System Requirements
Hardware: Microphone, speakers/headphones

Software: Python 3.x, required libraries

OS: Windows, macOS, or Linux

## Installation

Install Python from: https://www.python.org/downloads/

Download or clone this repository.

Open a terminal or command prompt in the project directory and run: python language_translator.py

## How It Works
Captures user speech via microphone.

Converts it to text using SpeechRecognition.

Translates text with Google Translate API.

Converts translated text to speech with gTTS.

Plays back the translated audio output.

## Supported Languages
Supports major global languages including English, Urdu, Spanish, French, German, Arabic, Chinese, and more (as supported by Google APIs).

## Error Handling
Alerts if audio is unclear or mic is disconnected.

Handles unsupported languages or failed translations.

Displays user-friendly messages for unexpected errors.
