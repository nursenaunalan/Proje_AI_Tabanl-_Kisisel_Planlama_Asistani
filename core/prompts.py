# core/prompts.py

SYSTEM_PROMPT = "Sen profesyonel bir zaman yönetimi asistanısın. Görevin, verilen metinden görevleri ayıklamak, önceliklendirmek ve planlamaktır. Yanıtlarını her zaman geçerli bir JSON listesi olarak ver."

EXTRACTOR_PROMPT = """
Aşağıdaki metinden görevleri bul ve JSON listesi yap.
Hızlı ve sadece veriye odaklan.

JSON: [{{"task_name": "...", "duration": int, "deadline": "HH:MM/null"}}]

Metin: {user_input}
"""

PRIORITIZER_PROMPT = """
Bu görevleri Eisenhower Matrisi'ne göre değerlendir. Yanıtın SADECE bir JSON listesi olmalı.
Kategoriler: "🔥 KRİTİK", "📅 STRATEJİK", "⚡ OPERASYONEL", "🗑️ ERTELENEBİLİR"

JSON SCHEMA:
[
  {{"task_name": "string", "importance": integer 1-10, "urgency": integer 1-10, "category": "string"}}
]

Görevler: {tasks}
"""

SCHEDULER_PROMPT = """
09:00'dan başlayan bir günlük program yap. Yanıtın SADECE bir JSON listesi olmalı.
Çakışma yapma, aralara 10'ar dakika mola koy.

JSON SCHEMA:
[
  {{"time": "HH:MM - HH:MM", "task": "string", "note": "string"}}
]

Görevler: {prioritized_tasks}
"""
