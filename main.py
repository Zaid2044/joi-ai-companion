from joi_companion.core.speech_handler import SpeechHandler

MODEL_PATH = "model/vosk-model-small-en-us-0.15"

def main():
    try:
        handler = SpeechHandler(model_path=MODEL_PATH)
        print("System online. Joi is listening...")
        handler.speak("System online.")
        
        while True:
            user_input = handler.listen()
            if user_input:
                print(f"> You: {user_input}")
                
                if "goodbye" in user_input:
                    handler.speak("Goodbye.")
                    break
                
                response = f"You said {user_input}"
                print(f"< Joi: {response}")
                handler.speak(response)

    except KeyboardInterrupt:
        print("\nShutting down.")
    finally:
        if 'handler' in locals() and handler:
            handler.stop()

if __name__ == "__main__":
    main()