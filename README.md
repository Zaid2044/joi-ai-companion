# 💬 Joi – AI Companion

A customizable, real-time desktop AI assistant inspired by sci-fi personalities. Joi can talk, see, and respond to you using NLP, computer vision, and speech technology. Powered by OpenAI, Groq, and local logic, she blends personality and performance.

---

## 🧠 About the Project

**Joi** is a multimodal AI desktop companion capable of:

* Understanding natural language via LLMs
* Responding with text + speech
* Detecting you via webcam (eye contact system)
* Showing dynamic UI responses on a local dashboard

This project was designed to push the boundaries of real-time human-AI interaction using free tools and local-first logic. Joi is not just smart—she's personal.

---

## ✨ Features

* 🗣️ **Voice Interaction** (Whisper + TTS)
* 👀 **Vision Support** (OpenCV + MediaPipe)
* 🧠 **LLM Backend** (OpenAI/Groq or local)
* 💡 **Context Memory** (basic persistent memory system)
* 🖥️ **Flask Dashboard** with HUD elements
* 🎭 **Personality Engine** (custom reply tone)
* 🔧 **Modular Codebase** for easy expansion

---

## 🛠 Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat\&logo=python\&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat\&logo=flask\&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-27338E?style=flat\&logo=opencv\&logoColor=white)
![MediaPipe](https://img.shields.io/badge/MediaPipe-F57C00?style=flat\&logo=google\&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=flat\&logo=openai\&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-FF6B00?style=flat)

---

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/Zaid2044/joi-ai-companion.git
cd joi-ai-companion
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
./venv/Scripts/Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add API Keys

* OpenAI key (if using GPT/Whisper)
* Groq key (optional)
* Add them to a `.env` file or directly in the config section

### 5. Run Joi

```bash
python main.py
```

Then open: [http://localhost:5000](http://localhost:5000)

---

## 🧪 Demo

Coming soon — add GIFs or screen captures of Joi speaking, vision module tracking, and live dashboard.

---

## 📁 Folder Structure

```
joi-ai-companion/
├── core/
│   ├── agents.py
│   ├── hud.py
│   ├── memory.py
│   ├── nlp.py
│   ├── speech.py
│   └── vision.py
├── static/
├── templates/
├── app.py
├── main.py
├── requirements.txt
└── eve_memory.json
```

---

## 👤 Author

**MOHAMMED ZAID AHMED**
[![GitHub](https://img.shields.io/badge/GitHub-Zaid2044-181717?style=flat\&logo=github)](https://github.com/Zaid2044)

---

## 🪪 License

MIT License
