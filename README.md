# Resd AutoMouse

    자동 클릭을 도와주는 마우스 매크로

 게임같은 환경에서 매크로 감지를 피하기 위한 랜덤 지연 기능을 포함하고 있습니다.

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python)
![GUI](https://img.shields.io/badge/GUI-Tkinter-green?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

## 주요 기능 (Key Features)

* **오토 클릭:** 좌클릭/우클릭 지원 및 속도 조절 가능
* **감지 방지:** 랜덤 지연 시간을 추가하여 사람처럼 자연스러운 클릭 구현
* **좌표 고정:** 마우스 커서 위치와 상관없이 지정된 좌표만 클릭하는 기능
* **다국어 지원:** 한국어, English, 日本語, 中文 지원


## 설치 및 실행 방법 (Download & Run)

소스 코드를 직접 실행하거나, 배포된 실행 파일(.exe)을 다운로드하여 사용할 수 있습니다.

### 1. 실행 파일로 사용하기 (추천)
우측 사이드바의 **[Releases]** 메뉴에서 최신 버전(`v1.0.0`)의 `Resd_AutoMouse.exe`를 다운로드하여 실행하세요.
(별도의 설치 없이 바로 실행됩니다.)

### 2. 소스 코드로 실행하기
Python이 설치된 환경에서 아래 명령어로 라이브러리를 설치 후 실행합니다.

```bash
# 레포지토리 클론
git clone [https://github.com/본인아이디/Resd-AutoMouse.git](https://github.com/본인아이디/Resd-AutoMouse.git)

# 필수 라이브러리 설치
pip install pynput

# 실행
python gui_clicker.py
```

## ⚠️ 주의사항 및 면책 조항

이 프로그램은 개인적인 학습 및 자동화 테스트 목적으로 개발했습니다.

사용자는 이 프로그램을 실행함에 있어 다음 사항을 숙지하고 동의하는 것으로 간주합니다:

1.  **사용 책임:** 본 프로그램을 특정 게임, 웹사이트, 서비스 등에서 사용하여 발생하는 모든 불이익(계정 정지, 밴, 서비스 이용 제한 등)에 대한 책임은 **전적으로 사용자 본인**에게 있습니다.
2.  **약관 준수:** 사용하려는 대상 서비스의 이용 약관을 반드시 확인하시기 바랍니다. 자동화 소프트웨어(매크로) 사용을 금지하는 곳에서는 절대 사용하지 마세요.
3.  **면책:** 개발자는 이 프로그램의 오용으로 인해 발생하는 어떠한 직·간접적인 피해에 대해서도 법적 책임을 지지 않습니다.

---