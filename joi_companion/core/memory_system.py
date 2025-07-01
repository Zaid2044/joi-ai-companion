from tinydb import TinyDB, Query
from datetime import datetime
import random

class MemorySystem:
    def __init__(self, db_path='joi_memory.json'):
        self.db = TinyDB(db_path)
        self.conversations = self.db.table('conversations')

    def log_interaction(self, user_input, joi_response, user_emotion, joi_mode):
        self.conversations.insert({
            'timestamp': datetime.utcnow().isoformat(),
            'user_input': user_input,
            'joi_response': joi_response,
            'user_emotion_at_time': user_emotion,
            'joi_mode_at_time': joi_mode
        })

    def get_random_interaction(self):
        all_interactions = self.conversations.all()
        if all_interactions:
            return random.choice(all_interactions)
        return None
    
    def get_interaction_count(self):
        return len(self.conversations)

    def close(self):
        self.db.close()