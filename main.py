import cv2
import pygame
import threading
import queue
from pathlib import Path
from joi_companion.core.speech_handler import SpeechHandler
from joi_companion.core.vision_processor import VisionProcessor
from joi_companion.core.personality_engine import PersonalityEngine
from joi_companion.core.intent_parser import IntentParser
from joi_companion.core.memory_system import MemorySystem
from joi_companion.core.ui_manager import UIManager

ROOT_DIR = Path(__file__).parent
MODEL_PATH = str(ROOT_DIR / "model" / "vosk-model-small-en-us-0.15")
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

def speech_worker(handler, text_queue):
    while True:
        user_input = handler.listen()
        if user_input:
            text_queue.put(user_input)

def main():
    pygame.init()
    
    ui = UIManager(WINDOW_WIDTH, WINDOW_HEIGHT)
    clock = pygame.time.Clock()
    
    cap = cv2.VideoCapture(0)
    
    try:
        speech_handler = SpeechHandler(model_path=MODEL_PATH)
        vision_processor = VisionProcessor()
        personality_engine = PersonalityEngine()
        intent_parser = IntentParser()
        memory = MemorySystem()
        text_queue = queue.Queue()

        listen_thread = threading.Thread(target=speech_worker, args=(speech_handler, text_queue), daemon=True)
        listen_thread.start()
        
        print("System online. Joi is running.")
        
        current_emotion = "NEUTRAL"
        joi_last_response = personality_engine.get_greeting()
        user_last_input = ""
        
        speech_handler.speak(joi_last_response)
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            try:
                user_input = text_queue.get_nowait()
                user_last_input = user_input
                print(f"> You: {user_input}")

                intent = intent_parser.parse(user_input)
                
                response = ""
                interaction_to_log = True

                if intent["type"] == "CHANGE_PERSONALITY":
                    new_mode = intent["payload"]
                    response = personality_engine.set_mode(new_mode)
                    interaction_to_log = False
                
                elif intent["type"] == "EXIT":
                    response = "Goodbye. It was a pleasure."
                
                elif intent["type"] == "CONVERSE":
                    response = personality_engine.generate_response(current_emotion, memory_system=memory)
                
                else: 
                    response = "I'm not sure what you mean by that."
                
                joi_last_response = response
                
                if response:
                    print(f"< Joi: {response}")
                    ui.update_speaking_status(True)
                    speech_handler.speak(response)
                    ui.update_speaking_status(False)
                    if interaction_to_log:
                        memory.log_interaction(user_input, response, current_emotion, personality_engine.current_mode)

                if intent["type"] == "EXIT":
                    running = False

            except queue.Empty:
                pass

            success, frame = cap.read()
            if not success:
                continue

            processed_frame, current_emotion = vision_processor.process_frame(frame)
            
            ui.draw_background(processed_frame)
            ui.draw_avatar()
            ui.draw_ui_text(current_emotion, personality_engine.current_mode, memory.get_interaction_count())
            ui.draw_dialogue("", joi_last_response)
            
            ui.update_display()
            clock.tick(30)

    except KeyboardInterrupt:
        print("\nShutdown initiated.")
    finally:
        if 'speech_handler' in locals():
            speech_handler.stop()
        if 'vision_processor' in locals():
            vision_processor.close()
        if 'memory' in locals():
            memory.close()
        cap.release()
        pygame.quit()

if __name__ == "__main__":
    main()