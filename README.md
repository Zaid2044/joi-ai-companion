# Project Joi - The AI Emotional Companion

![Joi Demo](link_to_your_demo_gif_or_screenshot.png)

Project Joi is a real-time, local-first AI emotional companion inspired by the character from *Blade Runner 2049*. Operating entirely offline on a standard laptop, Joi interacts through voice and visual perception. She analyzes the user's facial expressions to understand their emotional state and adapts her personality, dialogue, and tone in response. With a persistent memory, Joi remembers past conversations, creating a uniquely personal and evolving user experience.

---

## 核心功能 (Core Features)

*   **Real-time Emotion Recognition:** Uses OpenCV and MediaPipe Face Mesh to analyze the user's facial expressions (Happy, Sad, Neutral) in real-time.
*   **Dynamic Personality Engine:** Joi can switch between different personality modes (e.g., Caring, Playful), which fundamentally alters her response style and vocabulary.
*   **Voice-Powered Interaction:** All interaction is handled through natural voice commands, powered by the offline Vosk STT engine and a pyttsx3 TTS engine.
*   **NLP Intent Parsing:** A `spaCy`-based intent parser understands user commands, distinguishing between conversation, commands to change personality, and exit cues.
*   **Persistent Memory System:** Joi uses a `TinyDB` JSON database to log all interactions, allowing her to recall details from past conversations to create a sense of continuity.
*   **Holographic UI:** A custom `Pygame` interface provides a stylized, futuristic aesthetic, complete with a reactive "avatar" that pulses when Joi speaks.
*   **100% Offline:** No internet connection or cloud APIs are required. All processing, from speech recognition to emotion analysis, happens locally.

---

## 🛠️ 技术栈 (Tech Stack)

*   **Programming Language:** Python 3
*   **Computer Vision:** OpenCV, MediaPipe
*   **Speech-to-Text (STT):** Vosk
*   **Text-to-Speech (TTS):** pyttsx3
*   **Natural Language Processing (NLP):** spaCy
*   **Database:** TinyDB (for local JSON storage)
*   **UI & Graphics:** Pygame

---

## ⚙️ Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Zaid2044/joi-ai-companion.git
    cd joi-ai-companion
    ```

2.  **Create a Python virtual environment:**
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\Activate.ps1
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install the required dependencies:**
    *Note: This project requires specific versions for compatibility between `mediapipe` and `spacy`.*
    ```bash
    pip install numpy==1.26.4
    pip install mediapipe==0.10.11
    pip install spacy==3.7.2
    pip install opencv-python pygame vosk pyttsx3 pyaudio tinydb
    ```

4.  **Download the language models:**
    ```bash
    # Download the spaCy model
    python -m spacy download en_core_web_sm

    # Download the Vosk model
    # 1. Visit https://alphacephei.com/vosk/models and download the "vosk-model-small-en-us-0.15" model.
    # 2. Create a 'model' folder in the root of the project.
    # 3. Unzip the contents into the 'model' folder.
    ```

5.  **Run the application:**
    ```bash
    python main.py
    ```

---

## 🎤 Usage

*   **Start the program:** Run `main.py`. Joi will greet you.
*   **Converse Naturally:** Speak to Joi. She will respond based on her current personality and your detected emotion.
*   **Change Personality:** Say "Set personality to playful" or "Change to caring" to switch her mode.
*   **Exit:** Say "goodbye" or "exit" to shut down the application gracefully.