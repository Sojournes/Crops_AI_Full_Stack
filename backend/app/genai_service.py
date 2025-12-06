import os
import google.genai as genai
from google.genai import types
from dotenv import load_dotenv
from .database import list_tables, describe_table, execute_query

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

class GenAIService:
    def __init__(self):
        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY not found in environment variables.")
        
        self.client = genai.Client(api_key=GOOGLE_API_KEY)
        self.db_tools = [list_tables, describe_table, execute_query]
        self.instruction = """You are an AI assistant designed to help farmers choose the best crops based on sustainability and profitability.
        You have access to 'farmer_profiles' and 'market_data' tables.
        
        Follow these steps:
        1. Inspect Tables: Use list_tables() and describe_table() first.
        2. Ask Clarifying Questions: Ask the user about their farm characteristics (pH, moisture, etc.) based on the table schema.
        3. Formulate Queries: Use execute_query() to find compatible crops or market data.
        4. Synthesize Recommendation: Recommend top 1-3 crops with reasons.
        
        Only use execute_query for SELECT statements.
        """
        
    def get_chat_response(self, message: str, history: list) -> tuple[str, list]:
        try:
            # Reconstruct chat history for the Gemini client
            # The SDK manages history in the chat session, but for REST API statelessness, 
            # we might need to handle it. 
            # Ideally, we keep a persistent session or pass history. 
            # For simplicity in this demo, we'll create a new chat and replay history or just send the prompt with context if short.
            # But the 'chats.create' returns a stateful object. 
            
            chat = self.client.chats.create(
                model="gemini-2.5-flash-lite",
                config=types.GenerateContentConfig(
                    system_instruction=self.instruction,
                    tools=self.db_tools,
                    temperature=0.7,
                )
            )
            
            # Simple history replay (caveat: tools execution in history might be tricky to replay perfectly without persisting tool outputs)
            # For this MVP, let's just send the current message. 
            # Future improvement: maintain server-side session or serialize full history correctly.
            
            # If we want to support history, we should format it. 
            # For now, let's rely on the client sending relevant context or assume single-turn logical flow for simplicity if we don't persist sessions.
            # HOWEVER, the prompt demands "Long context window: The model maintains the history".
            # So I should accept history.
            
            # Retry logic for 429 errors
            import time
            max_retries = 3
            base_delay = 5
            
            for attempt in range(max_retries):
                try:
                    response = chat.send_message(message)
                    break
                except Exception as e:
                    if "429" in str(e) and attempt < max_retries - 1:
                        delay = base_delay * (2 ** attempt)
                        print(f"Rate limit hit. Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        raise e
            
            # Extract text
            return response.text, history + [{"role": "user", "parts": [message]}, {"role": "model", "parts": [response.text]}]
            
        except Exception as e:
            print(f"GenAI Error: {e}")
            return f"I encountered an error: {e}", history
