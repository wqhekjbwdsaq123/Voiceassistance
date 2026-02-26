# 🎙️ 인공지능 음성 비서 (AI Voice Assistant)

> 🔗 **서비스 링크:** [https://voiceassistance-qzsmmkjsdfazd3scxgkiqq.streamlit.app/](https://voiceassistance-qzsmmkjsdfazd3scxgkiqq.streamlit.app/)

음성으로 질문하고 답변을 들을 수 있는 웹 기반의 인공지능 비서 애플리케이션입니다. 
Streamlit을 활용해 만들어졌으며, 사용하기 쉽고 깔끔한 인터페이스를 자랑합니다.

## ✨ 주요 기능 (Features)

*   **음성 인식 (STT, Speech-to-Text):** 마이크로 말한 한국어/영어 음성을 OpenAI Whisper API를 사용하여 텍스트로 정확하게 변환합니다.
*   **인공지능 대화 (LLM):** 변환된 텍스트를 OpenAI ChatGPT (GPT-4o 등) 모델에 전달하여, 맥락에 맞는 똑똑한 답변을 생성합니다.
*   **음성 합성 (TTS, Text-to-Speech):** 챗봇이 작성한 답변을 Google TTS(gTTS)를 통해 사람의 목소리처럼 자연스러운 한국어 음성으로 읽어줍니다.
*   **직관적인 대시보드 UI:** 
    *   **왼쪽 (질문하기):** 녹음 버튼과 직전에 녹음한 내 목소리를 다시 들어볼 수 있는 오디오 플레이어가 있습니다.
    *   **오른쪽 (대화 내용):** 카카오톡처럼 사용자와 인공지능이 나눈 대화 기록이 예쁜 말풍선 형태로 쌓입니다.

---

## 🚀 설치 및 실행 방법

### 1️⃣ 준비물
*   **Python 버젼:** Python 3.9 이상
*   **OpenAI API 키:** [OpenAI 홈페이지](https://platform.openai.com/api-keys)에서 발급받은 `sk-...` 로 시작하는 비밀 키가 필요합니다.

### 2️⃣ 로컬 컴퓨터에서 바로 실행하기

터미널이나 명령 프롬프트를 열고 아래 순서대로 명령어를 입력하세요.

1. **필수 라이브러리 설치하기:**
   ```bash
   pip install -r requirements.txt
   ```

2. **앱 실행하기:**
   ```bash
   streamlit run app.py
   ```

3. **브라우저에서 접속하기:**
   이후 인터넷 브라우저가 자동으로 뜨면서 페이지가 열립니다. (실행되지 않는다면 `http://localhost:8501` 로 접속하세요.)
   접속 후 화면 왼쪽 사이드바에 **OpenAI API Key**를 입력하면 음성 대화를 시작할 수 있습니다.

---

## 🛠️ 사용된 기술 스택 (Tech Stack)

*   **웹 프레임워크:** [Streamlit](https://streamlit.io/) (빠른 파이썬 웹앱 제작 툴)
*   **음성 인식/AI 모델:** [OpenAI API](https://openai.com/) (Whisper & ChatGPT)
*   **음성 생성:** `gTTS` (Google Text-to-Speech)
*   **오디오 처리:** `pydub`, `streamlit-audiorecorder`

---

## 💡 사용 팁
*   녹음이 끝난 뒤 사이드바 왼쪽에 있는 톱니바퀴 아래에서 `Clear Conversation(대화 지우기)` 버튼을 누르면, 모든 대화 기록과 플레이어가 초기화되어 새로운 마음으로 다시 질문할 수 있습니다!
