# core/prompts.py

SYSTEM_PROMPT = "Sen profesyonel bir zaman yönetimi asistanısın. Görevin, verilen metinden görevleri ayıklamak, önceliklendirmek ve planlamaktır. Yanıtlarını her zaman geçerli bir JSON listesi olarak ver."

EXTRACTOR_PROMPT = """
Aşağıdaki kullanıcı metninden yapılacak işleri (görevleri) ayıkla.
Her görev için şu alanları içeren bir JSON listesi döndür:
- task_name: Görevin adı
- duration: Tahmini süre (dakika cinsinden tam sayı)
- deadline: Varsa saat (HH:MM), yoksa null

Kullanıcı Metni: {user_input}
"""

PRIORITIZER_PROMPT = """
Aşağıdaki görevleri analiz et ve her biri için önem, aciliyet puanı (1-10) ve kategori ata.
Kategoriler: "🔥 KRİTİK", "📅 STRATEJİK", "⚡ OPERASYONEL", "🗑️ ERTELENEBİLİR".
JSON listesi olarak döndür.

Görevler: {tasks}
"""

SCHEDULER_PROMPT = """
Aşağıdaki görevleri kullanarak saat 09:00'dan başlayan, çakışmayan bir günlük program oluştur.
Her görev için zaman aralığı (time), görev adı (task) ve kısa bir not (note) içeren bir JSON listesi döndür.

Görevler: {prioritized_tasks}
"""
