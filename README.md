# 📅 AI Agent Tabanlı Kişisel Planlama Asistanı

Bu proje, kullanıcının günlük karmaşasını organize eden, görevlerini analiz edip önceliklendiren ve optimize edilmiş bir zaman planı sunan akıllı bir asistandır.

## 🚀 Temel Özellikler

- 🧠 **Doğal Dil İşleme:** Serbest metin halindeki görevleri otomatik olarak ayıklar.
- 🎯 **Eisenhower Matrisi:** Görevleri Önem ve Aciliyet kriterlerine göre 4 çeyreğe böler.
- 📅 **Akıllı Çizelge:** Görevlerin sürelerini ve önceliklerini dikkate alarak 09:00'dan başlayan bir günlük akış oluşturur.
- 🔗 **Prompt Zinciri:** TaskExtractor -> Prioritizer -> Scheduler ajanları arasında veri akışı sağlar.
- ⚡ **FastAPI & Streamlit:** Modern bir backend mimarisi ve şık bir kullanıcı arayüzü sunar.

## 🛠️ Mimari Şema

1.  **Frontend (Streamlit):** Kullanıcı etkileşimi ve görselleştirme.
2.  **Backend (FastAPI):** API yönetimi ve orkestrasyon.
3.  **Core (Gemini Agents):** 
    - `TaskExtractor`: Metinden yapılandırılmış veri çıkarır.
    - `Prioritizer`: Puanlama ve kategorizasyon yapar.
    - `Scheduler`: Zaman planı üretir.

## 📦 Kurulum

1.  **Bağımlılıkları Yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **API Anahtarını Ayarlayın:**
    `.env` dosyasına Google Gemini API anahtarınızı ekleyin:
    ```env
    GEMINI_API_KEY=sizin_api_anahtariniz
    ```

3.  **Backend'i Başlatın:**
    ```bash
    uvicorn backend.main:app --reload
    ```

4.  **Frontend'i Başlatın:**
    ```bash
    streamlit run app.py
    ```

## 🔐 Güvenlik ve Gizlilik

- API anahtarları `.env` dosyası üzerinden yönetilir ve `.gitignore` ile korunur.
- Kullanıcı verileri yerel olarak işlenir ve saklanmaz.

## 📌 Kullanım Senaryosu

"Bugün saat 14:00'e kadar bir sunum hazırlamam lazım, öğle arasında spor salonuna gitmek istiyorum, akşam için marketten malzeme alıp yemek yapmalıyım ve 30 dakika kitap okumalıyım."

Girdiğiniz bu metin, sistem tarafından otomatik olarak parçalara ayrılır, önem sırasına konur ve size en uygun saat dilimleriyle birlikte sunulur.
