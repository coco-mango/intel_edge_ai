import streamlit as st
from audiorecorder import audiorecorder
import openai
import os
from datetime import datetime
from gtts import gTTS
import base64


def TTS(response): # gTTS를 활용하여 음성 파일 생성
    filename = "output.mp3"
    tts = gTTS(text=response, lang="ko")
    tts.save(filename)

    # 음원 파일 자동 재생
    with open(filename, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio autoplay = "Treu">
            <source src = "data:audio/mp3;base64, {b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(md, unsafe_allow_html=True,)
    #파일 삭제
    os.remove(filename)

# 음성파일 -> 텍스트
def TTS(audio):
    filename='input.mp3'
    audio.export(filename, format="mp3")  # 파일 저장
    audio_file = open(filename,"rb")      # 파일 열기
    transcript = openai.Audio.transcribe("whister-1",audio_file)   # Whisper 모델을 활용하여 텍스트 얻기
    audio_file.close()   
    os.remove(filename)     #파일 삭제
    return transcript["text"]

def ask_gpt(prompt, model):
    response = openai.ChatCompletion.create(model=model, messages=prompt)
    system_message = response["choices"][0]["message"]
    return system_message["content"]

# 메인 함수
def main():
    # 기본 설정
    st.set_page_config(
        page_title="음성 비서 프로그램", layout="wide")
    # 제목
    st.header("음성 비서 프로그램")   
    # 구분선
    st.markdown("---")

    # 기본 설명
    with st.expander("음성 비서 프로그램에 관하여", expanded=True):
        st.write(
            """
            - 음성비서 프로그램의 UI는 스트림릿을 활용했습니다.
            - STT(Speach-To-Text)는 OpenAI의 Whisper AI를 활용했습니다.
            - 답변은 OpenAI의 GPT 모델을 활용했습니다.
            - TTS(Text-To-Speech)는 구글의 Google Translate TTS를 활용했습니다.
            """)
        
        st.markdown("")

    # 사이드바 생성
    with st.sidebar:
        # Open AI API키 입력받기
        openai.api_key = st.text_input(label="OPENAI API키", placeholder="Enter your API key", value="", type="password")
        st.markdown("---")
        # GPT 모델을 선택하기 위한 라디오 버튼 생성
        model = st.radio(label="GPT 모델",options=["gpt-4","gpt-3.5-turbo"])
        st.markdown("---")
        # 리셋 버튼 생성
        if st.button(label="초기화"):
            # 리셋코드
            st.session_state["chat"] = []
            st.session_state["messages"] = [{"role":"system","content":"Yor are a thoghtful assistant. \
                                             Resopnd to all input in 25 words and answer in korea"}]
            st.session_state["check_reset"] = True
    # session state 초기화
    if "chat" not in st.session_state:
        st.session_state["chat"] = []
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role":"system","content":"Yor are a thoghtful assistant. \
                                        Resopnd to all input in 25 words and answer in korea"}]
    if "check_reset" not in st.session_state:
        st.session_state["check_reset"] = False
    
    # 기능 구현 공간
    col1, col2 = st.columns(2)
    with col1: #왼쪽 영역 작성
        st.subheader("질문하기")
        # 음성 녹음 아이콘 추가
        audio = audiorecorder("클릭하여 녹음하기","녹음중...")
        if (audio.duration_seconds > 0) and (st.session_state["check_reset"]==False):
            st.audio(audio.expert().read())   # 음성재생
            question = STT(audio)     #음성 파일에서 텍스트 추출
            now = datetime.now().strftime("%H:%M")   # 채팅 시각화를 위해 질문내용 저장
            st.session_state["chat"] = st.session_state["chat"]+[("user",now,question)]
            st.session_state["messages"] = st.session_state["messages"]+[{"role":"user","content":question}]   # GPT 모델에 넣을 프롬프트를 위해 질문내용 저장
    
    with col2: # 오른쪽 영역 작성
        st.subheader("질문/답변")
        if (audio.duration_seconds > 0) and (st.session_state["check_reset"]==False):
            response = ask_gpt(st.session_state["messages"],model)   # ChatGPT에게 답변 얻기
            st.session_state["messages"] = st.session_state["messages"]+[{"role":"system","content":response}]  # GPT 모델에 넣을 프롬프트를 위해 답변내용 저장
            now = datetime.now().strftime("%H:%M")   # 채팅 시각화를 위해 답변내용 저장
            st.session_state["chat"] = st.session_state["chat"]+[("bot",now,response)]
            # 채팅 형식으로 시각화하기
            for sender, time, message in st.session_state["chat"]:
                if sender == "user":
                    st.write(f'<div style="display:flex;align-items:center;">\
                             <div style="background-color:#007AFF;color:white;border-radius:12px;padding:8px 12px;margin-right:8px;">\
                             {message}</div><div style="font-size:0.8rem;color:gray;">{time}</div></div>', unsafe_allow_html=True)
                    st.write("")
                else:
                    st.write(f'<div style="displat:flex;align-items:center;justify-content:flex-end;">\
                             <div style="background-color:lightgray;border-radius:12px;padding:8px 12px;margin-left:8px;">\
                             {message}</div><div style="font-size:0.8rem;color:gray;">{time}</div></div>', unsafe_allow_html=True)
                    st.write("")
