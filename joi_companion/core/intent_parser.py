import spacy

class IntentParser:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.personality_keywords = ["caring", "playful", "romantic", "sarcastic"]

    def parse(self, text):
        doc = self.nlp(text.lower())
        
        intent = {
            "type": "UNKNOWN",
            "payload": None
        }

        change_personality_triggers = ["set", "change", "switch", "activate", "be"]
        found_trigger = any(token.lemma_ in change_personality_triggers for token in doc)
        
        if found_trigger:
            for token in doc:
                if token.text in self.personality_keywords:
                    intent["type"] = "CHANGE_PERSONALITY"
                    intent["payload"] = token.text.upper()
                    return intent

        if any(token.lemma_ in ["goodbye", "exit", "quit", "shutdown"] for token in doc):
            intent["type"] = "EXIT"
            return intent

        intent["type"] = "CONVERSE"
        return intent