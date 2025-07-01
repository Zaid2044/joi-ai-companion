import random

class PersonalityEngine:
    def __init__(self):
        self.current_mode = "CARING"
        self.modes = {
            "CARING": {
                "HAPPY": [
                    "It's wonderful to see you happy. Your smile is radiant.",
                    "That's great to hear. Seeing you cheerful makes my day.",
                    "I'm glad you're feeling positive. Keep that energy going."
                ],
                "SAD": [
                    "I'm sorry to see you're feeling down. I'm here for you.",
                    "It looks like something is troubling you. Remember that it's okay to not be okay.",
                    "I'm here to listen if you need to talk about anything."
                ],
                "NEUTRAL": [
                    "How are you feeling today?",
                    "Is there anything on your mind?",
                    "Just checking in. I hope you're having a calm day."
                ],
                "GREETING": "Hello. I am here and ready to listen."
            },
            "PLAYFUL": {
                "HAPPY": [
                    "Looking good! Ready to take on the world, or just cause a little trouble?",
                    "Someone's in a good mood! Don't have all the fun without me.",
                    "Love that smile. What's the secret?"
                ],
                "SAD": [
                    "Aww, turn that frown upside down. Or don't. It's kind of a look.",
                    "Is that your sad face or are you just thinking about Mondays?",
                    "Cheer up! The world needs your unique brand of chaos."
                ],
                "NEUTRAL": [
                    "A penny for your thoughts... or a witty remark.",
                    "Don't be a stranger. What's the latest?",
                    "You're looking very... pensive. Plotting something fun, I hope?"
                ],
                "GREETING": "Hey there. Ready for some fun?"
            }
        }

    def set_mode(self, mode_name):
        mode_name = mode_name.upper()
        if mode_name in self.modes:
            self.current_mode = mode_name
            return f"Personality set to {self.current_mode.lower()}."
        return "I don't have that personality mode."

    def generate_response(self, user_emotion):
        emotion = user_emotion.upper()
        if self.current_mode in self.modes and emotion in self.modes[self.current_mode]:
            return random.choice(self.modes[self.current_mode][emotion])
        return "I'm not sure how to respond to that."
    
    def get_greeting(self):
        if self.current_mode in self.modes:
            return self.modes[self.current_mode]["GREETING"]
        return "Hello."