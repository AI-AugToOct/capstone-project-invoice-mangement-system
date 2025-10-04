import streamlit as st
import requests

st.title("💬 Chat with your Invoices")

# ✅ Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Show chat history
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f"🧑 **You:** {msg['content']}")
    else:
        st.markdown(f"🤖 **AI:** {msg['content']}")

# Input box
question = st.text_input("Ask something about your invoices:")

if st.button("Ask"):
    if question.strip():
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": question})

        try:
            response = requests.post(
                "http://127.0.0.1:8000/chat/ask",
                json={"question": question, "top_k": 3},
            )

            if response.status_code == 200:
                data = response.json()

                ai_answer = data["answer"]
                st.session_state.chat_history.append({"role": "ai", "content": ai_answer})

                # Add matches if exist
                if data.get("matches"):
                    matches_text = "### 📄 Related invoices:\n"
                    for m in data["matches"]:
                        matches_text += (
                            f"- 🧾 Invoice {m['invoice_id']} from {m['vendor']} "
                            f"on {m['date']} → Total: {m['total']} SAR\n"
                        )
                    st.session_state.chat_history.append({"role": "ai", "content": matches_text})

                # 🔄 Refresh the page to show new messages
                st.rerun()
            else:
                st.error(f"❌ Error: {response.text}")

        except Exception as e:
            st.error(f"❌ Exception: {e}")
