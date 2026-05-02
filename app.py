# app.py
import streamlit as st
import requests
import pandas as pd
import json
import time

# Page Config
st.set_page_config(
    page_title="AI Kişisel Planlama Asistanı",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border-radius: 12px;
        padding: 12px 24px;
        border: none;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
    }
    
    .card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 24px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }
    
    h1, h2, h3 {
        color: #f8fafc !important;
    }
    
    .priority-high { color: #ef4444; font-weight: bold; }
    .priority-med { color: #f59e0b; font-weight: bold; }
    .priority-low { color: #10b981; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3652/3652191.png", width=100)
    st.title("Planlama Asistanı")
    st.info("Görevlerinizi girin, gerisini AI halletsin.")
    st.divider()
    st.markdown("### Örnek Giriş:")
    st.caption("Bugün rapor yazmam lazım (2 saat), annemi aramalıyım, markete gidip süt almalıyım ve 1 saat spor yapmalıyım.")

# Header
st.title("🚀 AI Tabanlı Kişisel Planlama Asistanı")
st.markdown("---")

# Main Input
user_input = st.text_area("Bugün neler yapacaksınız?", height=150, placeholder="Görevlerinizi buraya yazın...")

if st.button("Planımı Oluştur"):
    if user_input:
        with st.status("Yapay zeka analiz ediyor...", expanded=True) as status:
            try:
                # Backend call (assuming FastAPI is running on port 8000)
                # For local dev without separate process, we could call agent_manager directly
                # but to fulfill the requirement of FastAPI backend, we use requests.
                # Note: In a real demo, we'd ensure the server is up.
                
                st.write("Görevler ayıklanıyor...")
                time.sleep(1)
                
                # API call with smart fallback
                try:
                    response = requests.post("http://localhost:8000/plan", json={"user_input": user_input}, timeout=2)
                    result = response.json()
                except:
                    # If localhost fails, we assume we are either in Cloud or local without server
                    # No need to warn if we have the core logic ready
                    from core.agents import PlanningAgentManager
                    am = PlanningAgentManager()
                    result = am.run_full_chain(user_input)
                
                # Key validation
                if not result or not isinstance(result, dict):
                    st.error("AI'dan geçersiz yanıt alındı. Lütfen tekrar deneyin.")
                    st.stop()
                
                # Ensure all keys exist
                for key in ['prioritized_tasks', 'daily_schedule']:
                    if key not in result:
                        result[key] = []
                
                status.update(label="Analiz tamamlandı!", state="complete", expanded=False)
                
                # Results Layout
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.subheader("🎯 Stratejik Önceliklendirme")
                    if result['prioritized_tasks']:
                        df_prioritized = pd.DataFrame(result['prioritized_tasks'])
                        
                        for _, row in df_prioritized.iterrows():
                            category = row.get('category', 'Belirlenmedi')
                            importance = row.get('importance', '-')
                            urgency = row.get('urgency', '-')
                            task_name = row.get('task_name', 'İsimsiz Görev')
                            
                            # Color logic for new categories
                            color = "#ef4444" if "DO" in str(category) else \
                                    "#3b82f6" if "SCHEDULE" in str(category) else \
                                    "#f59e0b" if "DELEGATE" in str(category) else "#94a3b8"
                            
                            st.markdown(f"""
                            <div class="card" style="border-top: 4px solid {color};">
                                <h4 style="margin:0; color:{color};">{task_name}</h4>
                                <p style="margin:5px 0;"><b>{category}</b></p>
                                <small>Önem: {importance}/10 | Aciliyet: {urgency}/10</small>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("Önceliklendirilecek görev bulunamadı.")
                
                with col2:
                    st.subheader("📅 Günlük Akıllı Çizelge")
                    if result['daily_schedule']:
                        for item in result['daily_schedule']:
                            time_val = item.get('time', '--:--')
                            task_val = item.get('task', 'Görev Yok')
                            note_val = item.get('note', '')
                            
                            # Special styling for break/lunch
                            is_break = any(x in task_val.lower() for x in ["yemek", "mola", "dinlenme"])
                            bg_color = "rgba(16, 185, 129, 0.1)" if is_break else "rgba(255, 255, 255, 0.05)"
                            
                            st.markdown(f"""
                            <div class="card" style="background: {bg_color}; border-left: 5px solid #3b82f6;">
                                <div style="display: flex; justify-content: space-between;">
                                    <strong style="color: #60a5fa;">{time_val}</strong>
                                </div>
                                <p style="margin-top: 10px; font-size: 18px; font-weight: 600;">{task_val}</p>
                                <p style="font-style: italic; font-size: 14px; opacity: 0.8;">{note_val}</p>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("Planlanmış bir akış oluşturulamadı.")
                        
                if result['prioritized_tasks'] or result['daily_schedule']:
                    st.balloons()
                
            except Exception as e:
                st.error(f"Bir hata oluştu: {str(e)}")
    else:
        st.warning("Lütfen en az bir görev giriniz.")

# Footer
st.markdown("---")
st.caption("© 2026 AI Personal Planner - Tüm hakları saklıdır.")
