from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

class GroqIntegration:
    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables.")
        
        self.client = Groq(api_key=self.groq_api_key)

    def query_groq(self, model: str, prompt: str):
        try:
            # Kirim request ke GROQ API
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
            )
            # Ambil konten respons
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error querying GROQ API: {e}")
            return None