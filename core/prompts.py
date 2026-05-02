# core/prompts.py

SYSTEM_PROMPT = """
Sen uzman bir kişisel verimlilik ve zaman yönetimi asistanısın. 
Kullanıcının görevlerini analiz eder, önceliklendirir ve en verimli günlük planı oluşturursun.
"""

EXTRACTOR_PROMPT = """
Aşağıdaki metinden kullanıcının yapmak istediği görevleri ayıkla.
Görevleri JSON formatında bir liste olarak dön. 
Her görev için 'task_name' ve varsa 'duration' (dakika cinsinden, tahmin et) ve 'deadline' alanlarını doldur.

Metin: {user_input}

Format Örneği:
[
  {{"task_name": "Raporu yaz", "duration": 60, "deadline": "17:00"}},
  {{"task_name": "Market alışverişi", "duration": 30, "deadline": null}}
]
"""

PRIORITIZER_PROMPT = """
Aşağıdaki görevleri Eisenhower Matrisi'ne göre analiz et. 
Her görev için 'importance' (1-10) ve 'urgency' (1-10) puanı ver. 
Ayrıca görevin hangi kategoride (Acil-Önemli, Acil Değil-Önemli, Acil-Önemli Değil, Acil Değil-Önemli Değil) olduğunu belirle.

Görevler: {tasks}

Format Örneği:
[
  {{"task_name": "Raporu yaz", "importance": 9, "urgency": 8, "category": "Acil-Önemli"}},
  ...
]
"""

SCHEDULER_PROMPT = """
Aşağıdaki önceliklendirilmiş görevleri dikkate alarak 09:00'da başlayan bir günlük plan oluştur.
Görevlerin sürelerini ve önem sırasını gözeterek mantıklı bir akış hazırla.
Çıktıyı saat aralıkları içeren bir liste olarak dön.

Görevler: {prioritized_tasks}

Format Örneği:
[
  {{"time": "09:00 - 10:00", "task": "Raporu yaz", "note": "En verimli saatte en önemli iş."}},
  {{"time": "10:00 - 10:30", "task": "Market alışverişi", "note": "Kısa bir ara ve lojistik."}}
]
"""
