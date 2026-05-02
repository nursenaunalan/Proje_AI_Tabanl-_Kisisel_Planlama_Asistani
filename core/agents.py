# core/agents.py
import os
import json
import google.generativeai as genai
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
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def _call_gemini(self, prompt):
        try:
            response = self.model.generate_content([SYSTEM_PROMPT, prompt])
            if not response or not response.text:
                return []
            
            text = response.text
            # JSON bloğunu bulmaya çalış (```json ... ``` veya direkt [...])
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            
            # Başındaki/sonundaki gereksiz boşlukları temizle
            text = text.strip()
            
            # Eğer hala JSON gibi görünmüyorsa (köşeli parantez yoksa) 
            # ama model bir şekilde metin döndüyse, boş liste dönmektense 
            # basit bir temizleme yapalım.
            if not (text.startswith("[") or text.startswith("{")):
                # Metnin içindeki ilk [ veya { karakterini bul
                start_idx = -1
                for i, char in enumerate(text):
                    if char in "[{":
                        start_idx = i
                        break
                if start_idx != -1:
                    # Sondaki eşleşen karakteri bul
                    end_char = "]" if text[start_idx] == "[" else "}"
                    end_idx = text.rfind(end_char)
                    if end_idx != -1:
                        text = text[start_idx:end_idx+1]

            return json.loads(text)
        except Exception as e:
            print(f"Gemini/JSON Error: {str(e)}")
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
