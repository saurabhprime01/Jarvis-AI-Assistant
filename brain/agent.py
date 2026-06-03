import google.generativeai as genai
from app.core.config import settings
from loguru import logger
from typing import List, Dict, Any

class JarvisBrain:
    def __init__(self):
        if not settings.GOOGLE_API_KEY:
            logger.warning("GOOGLE_API_KEY not found in environment settings.")
        
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(settings.MODEL_NAME)
        self.chat_sessions = {} # userId -> chatSession

    async def get_response(self, user_id: str, message: str) -> str:
        """
        Generates a response from the LLM based on user input.
        """
        try:
            if user_id not in self.chat_sessions:
                self.chat_sessions[user_id] = self.model.start_chat(history=[])
            
            session = self.chat_sessions[user_id]
            response = await session.send_message_async(message)
            return response.text
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "I'm sorry, I'm having trouble processing your request right now."

jarvis_brain = JarvisBrain()
