import pygame
import numpy as np
import cv2
from pathlib import Path 

class UIManager:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        
        pygame.display.set_caption("Joi - AI Companion")
        font_dir = Path(__file__).parent.parent / "data" / "assets" / "fonts"
        
        self.font_path = str(font_dir / "Orbitron-VariableFont_wght.ttf")
        self.font_large = pygame.font.Font(self.font_path, 36)
        self.font_medium = pygame.font.Font(self.font_path, 28)
        self.font_small = pygame.font.Font(self.font_path, 20)

        self.colors = {
            "cyan": (0, 255, 255),
            "purple": (138, 43, 226),
            "white": (255, 255, 255),
            "black": (0, 0, 0),
            "transparent_black": (0, 0, 0, 180)
        }
        
        self.is_speaking = False
        self.avatar_pulse = 0

    def update_speaking_status(self, is_speaking):
        self.is_speaking = is_speaking

    def draw_background(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_flipped = cv2.flip(frame_rgb, 1)
        frame_surface = pygame.surfarray.make_surface(frame_flipped.swapaxes(0, 1))

        vignette = np.zeros_like(frame_flipped, dtype=np.uint8)
        cv2.circle(vignette, (self.width // 2, self.height // 2), self.width // 3, (255, 255, 255), -1)
        vignette = cv2.blur(vignette, (200, 200))
        
        masked_frame = cv2.bitwise_and(frame_flipped, vignette)
        
        final_frame_surface = pygame.surfarray.make_surface(masked_frame.swapaxes(0, 1))
        
        self.screen.fill(self.colors["black"])
        self.screen.blit(final_frame_surface, (0, 0))

    def draw_avatar(self):
        if self.is_speaking:
            self.avatar_pulse = (self.avatar_pulse + 5) % 255
            radius = 60 + (np.sin(pygame.time.get_ticks() * 0.02) * 10)
            color = self.colors["purple"]
        else:
            self.avatar_pulse = 0
            radius = 50
            color = self.colors["cyan"]
            
        pygame.draw.circle(self.screen, color, (self.width // 2, self.height - 100), radius, 2)
        
        overlay = self.screen.copy()
        pygame.draw.circle(overlay, color, (self.width // 2, self.height - 100), radius + 5, 10)
        overlay.set_alpha(50 + self.avatar_pulse // 2)
        self.screen.blit(overlay, (0,0))
        
    def draw_ui_text(self, emotion, mode, memories):
        info_surface = pygame.Surface((300, 150), pygame.SRCALPHA)
        info_surface.fill(self.colors["transparent_black"])
        
        emotion_text = self.font_medium.render(f"Emotion: {emotion}", True, self.colors["white"])
        info_surface.blit(emotion_text, (10, 10))
        
        mode_text = self.font_medium.render(f"Mode: {mode}", True, self.colors["white"])
        info_surface.blit(mode_text, (10, 50))
        
        memories_text = self.font_medium.render(f"Memories: {memories}", True, self.colors["white"])
        info_surface.blit(memories_text, (10, 90))
        
        self.screen.blit(info_surface, (20, 20))
        
    def draw_dialogue(self, user_text, joi_text):
        if joi_text:
            text_surface = self.font_large.render(joi_text, True, self.colors["cyan"])
            text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(text_surface, text_rect)

    def update_display(self):
        pygame.display.flip()