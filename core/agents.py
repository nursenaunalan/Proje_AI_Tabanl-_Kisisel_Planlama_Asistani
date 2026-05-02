import os
import json
from google import genai
from dotenv import load_dotenv
try:
    from core.prompts import SYSTEM_PROMPT, EXTRACTOR_PROMPT, PRIORITIZER_PROMPT, SCHEDULER_PROMPT
except ImportError:
    from prompts import SYSTEM_PROMPT, EXTRACTOR_PROMPT, PRIORITIZER_PROMPT, SCHEDULER_PROMPT

load_dotenv()

class PlanningAgentManager:
    def __init__(self):
        # API Keys - Check environment first, then st.secrets (for deployment)
        try:
            import streamlit as st
            self.api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")
        except:
            self.api_key = os.getenv("GEMINI_API_KEY")
            
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY bulunamadı! Lütfen .env dosyasını veya Streamlit Secrets ayarlarını kontrol edin.")
        
        self.client = genai.Client(api_key=self.api_key)
        self.model_id = 'gemini-1.5-flash'

    def _call_gemini(self, prompt):
        try:
            # New SDK prefers system_instruction in config or as a separate argument
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config={
                    'system_instruction': SYSTEM_PROMPT,
                    'response_mime_type': 'application/json',
                }
            )
            
            if not response or not response.text:
                return []
            
            # Since we used response_mime_type: application/json, 
            # text should be a clean JSON string.
            return json.loads(response.text.strip())
            
        except Exception as e:
            print(f"Gemini/JSON Error: {str(e)}")
            # Fallback for manual cleaning if needed
            try:
                text = response.text
                if "```json" in text:
                    text = text.split("```json")[1].split("```")[0].strip()
                elif "```" in text:
                    text = text.split("```")[1].split("```")[0].strip()
                return json.loads(text.strip())
            except:
                return []

    def extract_tasks(self, user_input):
        prompt = EXTRACTOR_PROMPT.format(user_input=user_input)
        result = self._call_gemini(prompt)
        return result if isinstance(result, list) else []

    def prioritize_tasks(self, tasks):
        if not tasks: return []
        prompt = PRIORITIZER_PROMPT.format(tasks=json.dumps(tasks, ensure_ascii=False))
        result = self._call_gemini(prompt)
        return result if isinstance(result, list) else []

    def generate_schedule(self, prioritized_tasks):
        if not prioritized_tasks: return []
        prompt = SCHEDULER_PROMPT.format(prioritized_tasks=json.dumps(prioritized_tasks, ensure_ascii=False))
        result = self._call_gemini(prompt)
        return result if isinstance(result, list) else []

    def run_full_chain(self, user_input):
        # Chain 1: Extraction
        tasks = self.extract_tasks(user_input)
        
        # Chain 2: Prioritization
        prioritized = self.prioritize_tasks(tasks)
        
        # Chain 3: Scheduling
        schedule = self.generate_schedule(prioritized)
        
        return {
            "original_tasks": tasks,
            "prioritized_tasks": prioritized,
            "daily_schedule": schedule
        }
