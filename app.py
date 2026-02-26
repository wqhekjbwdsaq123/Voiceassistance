import streamlit as st
from audiorecorder import audiorecorder
import openai
import os
from datetime import datetime
from gtts import gTTS
import base64

# --- Constants & Config ---
def STT(audio):
    filename = 'input.mp3'
    audio.export(filename, format="mp3")
    with open(filename, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
    os.remove(filename)
    return transcript["text"]

def ask_gpt(prompt_msgs, model):
    response = openai.ChatCompletion.create(model=model, messages=prompt_msgs)
    system_message = response["choices"][0]["message"]
    return system_message["content"]

def TTS(response_text):
    filename = "output.mp3"
    tts = gTTS(text=response_text, lang="ko")
    tts.save(filename)
    with open(filename, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio autoplay="True">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(md, unsafe_allow_html=True)
    os.remove(filename)

def main():
    st.set_page_config(
        page_title="AI Voice Assistant",
        page_icon="🎙️",
        layout="wide"
    )

    # Separate font and style for robustness
    st.markdown('<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap" rel="stylesheet">', unsafe_allow_html=True)
    
    css = """
    <style>
    * { font-family: 'Outfit', sans-serif; }
    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    .main .block-container { padding-top: 2rem; max-width: 1400px; }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.18);
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
        margin-bottom: 2rem;
    }
    
    .chat-bubble {
        padding: 12px 18px;
        border-radius: 18px;
        margin-bottom: 12px;
        font-size: 1rem;
        line-height: 1.5;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        max-width: 85%;
        animation: fadeIn 0.3s ease-in-out;
    }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    .user-bubble { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; margin-left: auto; border-bottom-right-radius: 4px; }
    .bot-bubble { background: white; color: #1a202c; margin-right: auto; border-bottom-left-radius: 4px; }
    .time-label { font-size: 0.7rem; color: #a0aec0; margin-top: 4px; }

    .premium-title {
        text-align: center;
        background: -webkit-linear-gradient(left, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 600;
        font-size: 3rem;
        margin-bottom: 0.1rem;
    }
    .premium-subtitle { text-align: center; color: #718096; margin-bottom: 2rem; font-size: 1.1rem; }
    
    /* Native container styling for left side card */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255, 255, 255, 0.7) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border-radius: 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.18) !important;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1) !important;
        padding: 1.5rem !important;
        margin-top: 0.5rem !important;
    }
    
    /* Chat container scrolling */
    .chat-container {
        height: 500px;
        overflow-y: auto;
        padding-right: 15px;
        margin-bottom: 0 !important;
    }
    
    /* Custom scrollbar */
    .chat-container::-webkit-scrollbar { width: 6px; }
    .chat-container::-webkit-scrollbar-thumb { background-color: rgba(160, 174, 192, 0.5); border-radius: 10px; }
    .chat-container::-webkit-scrollbar-track { background: transparent; }

    /* Styling for the audiorecorder button */
    .stButton button, .audiorecorder button, button[kind="secondary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 40px !important;
        padding: 15px 45px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        width: 280px !important;
        max-width: 90% !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    .stButton button:hover, .audiorecorder button:hover, button[kind="secondary"]:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5) !important;
    }
    
    [data-testid="stSidebar"] { background-color: rgba(255, 255, 255, 0.9) !important; }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

    # Session state initialization must come first
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "system", "content": "You are a friendly AI assistant. Please respond concisely in Korean."}]
    if "reset_pending" not in st.session_state:
        st.session_state["reset_pending"] = False
    if "latest_user_audio" not in st.session_state:
        st.session_state["latest_user_audio"] = None

    st.markdown('<h1 class="premium-title">AI Voice Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p class="premium-subtitle">Your intelligent, voice-powered companion</p>', unsafe_allow_html=True)
    
    # Korean Description
    st.markdown('''
        <p style="text-align: center; color: #4a5568; margin-bottom: 3rem; font-size: 1.05rem; line-height: 1.6; word-break: keep-all;">
            음성으로 질문하고 답변을 들을 수 있는 인공지능 비서입니다.<br>
            왼쪽의 <strong>녹음하기 버튼</strong>을 눌러 자유롭게 질문 내용을 입력해 보세요.
        </p>
    ''', unsafe_allow_html=True)

    # Sidebar for settings
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        user_api_key = st.text_input("OpenAI API Key", type="password", placeholder="Enter sk-...")
        if user_api_key:
            openai.api_key = user_api_key
        
        selected_model = st.selectbox("Intelligence Level", options=["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"], index=0)
        
        st.divider()
        if st.button("🗑️ Clear Conversation", use_container_width=True):
            st.session_state["chat_history"] = []
            st.session_state["messages"] = [{"role": "system", "content": "You are a friendly AI assistant. Please respond concisely in Korean."}]
            st.session_state["latest_user_audio"] = None
            st.session_state["reset_pending"] = True
            st.rerun()
        
        # Removed info box as requested

    # 2-Column Layout for Main Content
    col_left, col_right = st.columns([1, 1], gap="large")
    
    with col_left:
        st.markdown("### 🎤 질문하기")
        with st.container(border=True):
            st.markdown('<p style="color: #4a5568; margin-bottom: 1.5rem; font-weight: 600; font-size: 1.1rem; text-align: center;">여기를 눌러 녹음을 시작하세요👇</p>', unsafe_allow_html=True)
            
            # The audiorecorder button
            audio = audiorecorder("🎙️ 녹음하기", "🛑 녹음 중지")
            
            # Update session state if new audio is recorded
            if len(audio) > 0 and not st.session_state["reset_pending"]:
                st.session_state["latest_user_audio"] = audio.export(format="wav").read()
            
            # Playback if audio exists in session state
            if st.session_state["latest_user_audio"] is not None:
                st.markdown('<p style="color: #4a5568; margin-top: 2rem; margin-bottom: 0.5rem; font-weight: 600; font-size: 0.95rem;">🔊 제일 최근에 녹음한 질문:</p>', unsafe_allow_html=True)
                st.audio(st.session_state["latest_user_audio"], format="audio/wav")

    with col_right:
        st.markdown("### 💬 대화 내용")
        # Scrollable Chat Container
        st.markdown('<div class="glass-card chat-container">', unsafe_allow_html=True)
        if not st.session_state["chat_history"]:
            st.markdown('<p style="text-align: center; color: #a0aec0; padding: 5rem 0;">대화 내용이 여기에 표시됩니다.<br>왼쪽에서 첫 질문을 시작해 보세요.</p>', unsafe_allow_html=True)
        else:
            for role, time, text in st.session_state["chat_history"]:
                if role == "user":
                    st.markdown(f'''
                        <div style="display: flex; flex-direction: column; align-items: flex-end;">
                            <div class="chat-bubble user-bubble">{text}</div>
                            <div class="time-label user-time">{time}</div>
                        </div>
                    ''', unsafe_allow_html=True)
                else:
                    st.markdown(f'''
                        <div style="display: flex; flex-direction: column; align-items: flex-start;">
                            <div class="chat-bubble bot-bubble">{text}</div>
                            <div class="time-label bot-time">{time}</div>
                        </div>
                    ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if len(audio) > 0 and not st.session_state["reset_pending"]:
        if not user_api_key:
            st.error("Please provide an OpenAI API Key in the sidebar.")
        else:
            try:
                # Transcription
                with st.spinner("Processing your voice..."):
                    transcript_text = STT(audio)
                
                timestamp = datetime.now().strftime("%H:%M")
                st.session_state["chat_history"].append(("user", timestamp, transcript_text))
                st.session_state["messages"].append({"role": "user", "content": transcript_text})
                
                # GPT Response
                with st.spinner("Generating response..."):
                    bot_response = ask_gpt(st.session_state["messages"], selected_model)
                
                st.session_state["messages"].append({"role": "assistant", "content": bot_response})
                st.session_state["chat_history"].append(("bot", timestamp, bot_response))
                
                # Output TTS and rerun to update UI
                TTS(bot_response)
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

    if st.session_state["reset_pending"]:
        st.session_state["reset_pending"] = False

if __name__ == "__main__":
    main()
