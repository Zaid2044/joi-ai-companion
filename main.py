import cv2
import pygame
import threading
import queue
from joi_companion.core.speech_handler import SpeechHandler
from joi_companion.core.vision_processor import VisionProcessor

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

    cap = cv2.VideoCapture(0)
    
    try:
        speech_handler = SpeechHandler(model_path=MODEL_PATH)
        vision_processor = VisionProcessor()
        text_queue = queue.Queue()

        listen_thread = threading.Thread(target=speech_worker, args=(speech_handler, text_queue), daemon=True)
        listen_thread.start()
        
        print("System online. Joi is running.")
        speech_handler.speak("System online.")
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            try:
                user_input = text_queue.get_nowait()
                print(f"> You: {user_input}")
                if "goodbye" in user_input.lower():
                    speech_handler.speak("Goodbye.")
                    running = False
                    continue
                
                response = f"I am observing you."
                print(f"< Joi: {response}")
                speech_handler.speak(response)
            except queue.Empty:
                pass

            success, frame = cap.read()
            if not success:
                continue

            processed_frame = vision_processor.process_frame(frame)
            
            frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
            frame_flipped = cv2.flip(frame_rgb, 1)
            frame_surface = pygame.surfarray.make_surface(frame_flipped.swapaxes(0, 1))
            
            screen.blit(frame_surface, (0, 0))
            
            pygame.display.flip()
            clock.tick(30)

    except KeyboardInterrupt:
        print("\nShutting down.")
    finally:
        if 'speech_handler' in locals():
            speech_handler.stop()
        if 'vision_processor' in locals():
            vision_processor.close()
        cap.release()
        pygame.quit()

if __name__ == "__main__":
    main()