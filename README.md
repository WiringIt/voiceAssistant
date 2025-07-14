# 🎙️ Voice Assistant

This project is a Python-based voice assistant that uses **OpenAI's Whisper** for speech-to-text transcription. It captures audio input from the user, processes it using custom logic or NLP, and responds with speech using a Text-to-Speech engine.

---

## ✨ Features

- 🎧 Records voice from microphone
- 🧠 Uses OpenAI Whisper for accurate speech-to-text transcription
- 🗣️ Converts response text back to speech
- 🔌 Modular design — plug in your own logic/NLP/TTS systems
- 🛠️ Easily extendable for IoT, personal desktop assistant, or chatbot backends

---

## 📦 Tech Stack

| Component | Technology |
|----------|------------|
| Audio Capture | `PyAudio` / `sounddevice` |
| Speech-to-Text (ASR) | [`OpenAI Whisper`](https://github.com/openai/whisper) |
| Command Processing | Custom logic (can be extended with NLP tools like spaCy, Rasa, etc.) |
| Text-to-Speech | `gTTS` / `pyttsx3` / Coqui / Amazon Polly |
| Language | Python 3 |

---

## 🚀 Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/WiringIt/voiceAssistant.git
cd voiceAssistant
