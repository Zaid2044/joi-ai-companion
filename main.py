import cv2
import pygame
import threading
import queue
from joi_companion.core.speech_handler import SpeechHandler
from joi_companion.core.vision_processor import VisionProcessor
from joi_companion.core.personality_engine import PersonalityEngine
from joi_companion.core.intent_parser import IntentParser
from joi_companion.core.memory_system import MemorySystem


MODEL_PATH = "model/vosk-model-small-en-us-0.15"
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

def speech_worker(handler, text_queue):
    while True:
        user_input = handler.listen()
        if user_input:
            text_queue.put(user_input)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Joi - AI Companion")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 40)
    
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
        initial_greeting = personality_engine.get_greeting()
        speech_handler.speak(initial_greeting)
        
        current_emotion = "NEUTRAL"
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            try:
                user_input = text_queue.get_nowait()
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
                    speech_handler.speak(response)
                    running = False
                
                elif intent["type"] == "CONVERSE":
                    response = personality_engine.generate_response(current_emotion)
                
                else: 
                    response = "I'm not sure what you mean by that."
                
                if response and running:
                    print(f"< Joi: {response}")
                    speech_handler.speak(response)
                    if interaction_to_log:
                        memory.log_interaction(user_input, response, current_emotion, personality_engine.current_mode)

            except queue.Empty:
                pass

            success, frame = cap.read()
            if not success:
                continue

            processed_frame, current_emotion = vision_processor.process_frame(frame)
            
            frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
            frame_flipped = cv2.flip(frame_rgb, 1)
            frame_surface = pygame.surfarray.make_surface(frame_flipped.swapaxes(0, 1))
            
            screen.blit(frame_surface, (0, 0))
            
            ui_y = 20
            ui_x = 20
            
            emotion_text = font.render(f"EMOTION: {current_emotion}", True, (255, 255, 255))
            screen.blit(emotion_text, (ui_x, ui_y))
            
            ui_y += 40
            mode_text = font.render(f"MODE: {personality_engine.current_mode}", True, (255, 255, 255))
            screen.blit(mode_text, (ui_x, ui_y))
            
            ui_y += 40
            interaction_count = memory.get_interaction_count()
            memory_text = font.render(f"MEMORIES: {interaction_count}", True, (255, 255, 255))
            screen.blit(memory_text, (ui_x, ui_y))
            
            pygame.display.flip()
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