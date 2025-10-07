import streamlit as st
import requests
import os
import sys
from dotenv import load_dotenv

# Add parent directory to path to import theme
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from theme import get_light_theme_css

# Apply light theme CSS
st.markdown(get_light_theme_css(), unsafe_allow_html=True)

load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

st.title("💬 تحدث مع فواتيرك")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f"🧑 **أنت:** {msg['content']}")
    else:
        st.markdown(f"🤖 **الذكاء الاصطناعي:** {msg['content']}")

# Input
question = st.text_input("اسأل شيئاً عن فواتيرك:")

if st.button("اسأل"):
    if question.strip():
        st.session_state.chat_history.append({"role": "user", "content": question})
        try:
            response = requests.post(
                f"{BACKEND_URL}/chat/ask",
                json={"question": question, "top_k": 3},
            )
            if response.status_code == 200:
                data = response.json()
                ai_answer = data["answer"]
                st.session_state.chat_history.append({"role": "ai", "content": ai_answer})

                if data.get("matches"):
                    matches_text = "### 📄 الفواتير ذات الصلة:\n"
                    for m in data["matches"]:
                        matches_text += (
                            f"- 🧾 فاتورة {m['invoice_id']} من {m['vendor']} "
                            f"في {m['date']} ← الإجمالي: {m['total']} ريال\n"
                        )
                    st.session_state.chat_history.append({"role": "ai", "content": matches_text})

                st.rerun()
            else:
                st.error(f"❌ خطأ: {response.text}")
        except Exception as e:
            st.error(f"❌ استثناء: {e}")
