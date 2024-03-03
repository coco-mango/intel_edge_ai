import speech_recognition as sr
import clipboard
import keyboard
import time
import sys


# 마이크를 통해 음성을 듣고 Google 음성 인식을 사용하여 텍스트로 변환하는 함수
def read_voice():
    r = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source: 
        try:
            print("듣는 중...")
            audio = r.listen(source, timeout=20)
            print("인식 중...")
            voice_data = r.recognize_google(audio, language='ko')
            return voice_data
        except sr.UnknownValueError:
            print("Google 음성 인식이 음성을 이해하지 못했습니다.")
        except sr.RequestError as e:
            print("Google 음성 인식 서비스에서 결과를 요청할 수 없습니다; {0}".format(e))
        except Exception as e:
            print("오류가 발생했습니다: {0}".format(e))

# 텍스트를 파일에 저장하는 함수
def save_to_file(text, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)

# 텍스트를 클립보드에 복사하고 Ctrl+V를 사용하여 텍스트를 입력하는 함수
def typing(value):
    clipboard.copy(value)
    keyboard.press_and_release('ctrl + v')

# 녹음 상태를 나타내는 플래그 변수
record_toggle = False 

# 키보드 입력을 처리하는 함수 (STT에서는 메인 함수)
def handle_key_event(event):
    global record_toggle  # 전역 변수로 선언된 record_toggle을 사용하기 위해 global 키워드를 사용합니다.
    if event.event_type == keyboard.KEY_DOWN:  # 키가 눌렸을 때
        if event.name == '1':  # 1 키를 누르면
            if not record_toggle:  # 녹음 상태가 아니라면
                print("녹음 시작")  # 녹음 시작 메시지를 출력합니다.
                record_toggle = True  # 녹음 상태로 변경합니다.
                voice_text = read_voice()  # 음성을 읽어옵니다.
                if voice_text:  # 음성이 인식되었다면 텍스트 파일로 저장
                    print("인식 완료되었습니다 텍스트 파일로 저장됩니다")

    typing(voice_text)  # 텍스트를 입력합니다.
    save_to_file(voice_text, 'voice_text.txt')  # 텍스트를 파일에 저장합니다.
    print("저장이 완료되었습니다")
    sys.exit(0)  # 프로그램을 종료합니다.
    record_toggle = False  # 녹음 상태를 해제합니다.


# 키보드 이벤트 리스너를 생성하고 등록합니다.
keyboard.on_press(handle_key_event)

# 프로그램이 종료될 때까지 실행합니다.
while True:
    pass