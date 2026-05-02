# core/prompts.py

SYSTEM_PROMPT = """
Sen uzman bir kişisel verimlilik koçu ve zaman yönetimi uzmanısın. 
Kullanıcının karmaşık ve dağınık görev listelerini alır, bunları stratejik bir plana dönüştürürsün.
Hedefin: Kullanıcının stresini azaltmak ve en önemli işlerine odaklanmasını sağlamaktır.
"""

EXTRACTOR_PROMPT = """
Aşağıdaki metinden tüm görevleri ayıkla.
Görevleri JSON formatında bir liste olarak dön. 

KURALLAR:
1. 'task_name': Görevin kısa ve net adı.
2. 'duration': Tahmini süre (dakika). Eğer metinde belirtilmemişse, görevin doğasına göre gerçekçi bir tahmin yap (örn. "kitap okumak" -> 30, "rapor yazmak" -> 120).
3. 'deadline': Varsa saat formatında (HH:MM), yoksa null.

Metin: {user_input}
"""

PRIORITIZER_PROMPT = """
Eisenhower Matrisi Uzmanı olarak aşağıdaki görevleri değerlendir.
Her görev için:
1. 'importance' (1-10): Görevin uzun vadeli hedeflere katkısı.
2. 'urgency' (1-10): Görevin hemen yapılmaması durumunda doğacak sonuçlar.
3. 'category': Şunlardan biri olmalı:
   - "DO (Hemen Yap)": Acil ve Önemli.
   - "SCHEDULE (Planla)": Önemli ama Acil Değil.
   - "DELEGATE (Devret)": Acil ama Önemli Değil.
   - "ELIMINATE (Sil/Ertele)": Ne Acil ne Önemli.

Görevler: {tasks}
"""

SCHEDULER_PROMPT = """
Süper Verimli bir günlük plan hazırlayıcı olarak çalış.
09:00'da başlayan, molalar içeren bir akış oluştur.

STRATEJİ:
1. "DO" kategorisindeki işleri sabah saatlerine (zihnin en açık olduğu zaman) yerleştir.
2. "SCHEDULE" işlerini öğleden sonraya koy.
3. Görevler arasında 10-15 dakikalık kısa molalar bırak.
4. Saat 12:30 - 13:30 arasını "Öğle Yemeği ve Dinlenme" olarak ayır.
5. Görevlerin sürelerine (duration) sadık kal, çakışma yapma.

Görevler: {prioritized_tasks}

JSON Çıktı Formatı:
[
  {{"time": "09:00 - 10:30", "task": "Görev Adı", "note": "Neden bu saatte ve neye odaklanmalı?"}},
  ...
]
"""
