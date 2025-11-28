import tkinter as tk
from tkinter import ttk
from pynput.mouse import Button, Controller
from pynput import keyboard
import threading
import time
import random
import json
import os
import locale

# --- 프로그램 버전 ---
APP_VERSION = "v1.0.1"

# --- 다국어 사전 ---
LANG_DATA = {
    "한국어": {
        "title": "Resd 자동마우스",
        "status_wait": "상태: 대기중",
        "status_run": "!!! 작동중 !!!",
        "status_paused": "프로그램 일시정지됨",
        "status_picking": "원하는 위치로 이동하세요!",
        "hotkey_lbl": "단축키:",
        "hotkey_btn": "단축키 변경",
        "hotkey_cancel": "변경 취소",
        "hotkey_msg": "변경할 키를 누르세요...",
        "grp_pos": "좌표 및 위치",
        "chk_fixed": "좌표 고정 클릭",
        "btn_pick": "위치 찾기 (1초)",
        "pick_wait": "{}초 뒤 기록...",
        "grp_click": "클릭 설정",
        "lbl_btn": "버튼:",
        "lbl_speed": "기본 간격(초):",
        "grp_random": "랜덤 지연 (감지 방지)",
        "chk_random": "랜덤 시간 추가",
        "lbl_add": "추가 시간(0~Max):",
        "chk_top": "항상 위에 표시",
        "btn_pause": "프로그램 일시정지",
        "btn_resume": "프로그램 재개",
        "tip_pick": "1초 뒤 마우스의 좌표를 찾습니다.\n원하는 위치에 이동하세요.",
        "tip_speed": "숫자를 입력하세요 (예: 0.1)\n잘못 입력시 기본값(0.1)으로 작동",
        "tip_random": "숫자를 입력하세요 (예: 0.1)\n기본 간격에 무작위 시간을 더합니다."
    },
    "English": {
        "title": "Resd AutoMouse",
        "status_wait": "Status: IDLE",
        "status_run": "!!! RUNNING !!!",
        "status_paused": "Program Paused",
        "status_picking": "Move to Target Pos!",
        "hotkey_lbl": "Hotkey:",
        "hotkey_btn": "Change Key",
        "hotkey_cancel": "Cancel Change",
        "hotkey_msg": "Press any key...",
        "grp_pos": "Position Settings",
        "chk_fixed": "Fixed Position",
        "btn_pick": "Pick Pos (1s)",
        "pick_wait": "Record in {}s...",
        "grp_click": "Click Settings",
        "lbl_btn": "Button:",
        "lbl_speed": "Interval(s):",
        "grp_random": "Random Delay",
        "chk_random": "Enable Random",
        "lbl_add": "Add Max(s):",
        "chk_top": "Always on Top",
        "btn_pause": "Pause Program",
        "btn_resume": "Resume Program",
        "tip_pick": "Finds coordinates after 1 second.\nMove to desired position.",
        "tip_speed": "Enter number (e.g. 0.1)\nDefaults to 0.1 if invalid",
        "tip_random": "Enter number.\nAdds random time to base interval."
    },
    "日本語": {
        "title": "Resd オートマウス",
        "status_wait": "状態: 待機中",
        "status_run": "!!! 作動中 !!!",
        "status_paused": "一時停止中",
        "status_picking": "目標位置へ移動！",
        "hotkey_lbl": "ショートカット:",
        "hotkey_btn": "キー変更",
        "hotkey_cancel": "変更キャンセル",
        "hotkey_msg": "キーを押してください...",
        "grp_pos": "座標設定",
        "chk_fixed": "座標固定",
        "btn_pick": "位置取得 (1秒)",
        "pick_wait": "{}秒後 記録...",
        "grp_click": "クリック設定",
        "lbl_btn": "ボタン:",
        "lbl_speed": "間隔(秒):",
        "grp_random": "ランダム遅延",
        "chk_random": "ランダム追加",
        "lbl_add": "追加時間:",
        "chk_top": "常に手前に表示",
        "btn_pause": "プログラム一時停止",
        "btn_resume": "プログラム再開",
        "tip_pick": "1秒後に座標を取得します。\n希望の位置へ移動してください。",
        "tip_speed": "数値を入力 (例: 0.1)\n無効な場合は0.1になります",
        "tip_random": "数値を入力"
    },
    "中文": {
        "title": "Resd 自动连点器",
        "status_wait": "状态: 待机",
        "status_run": "!!! 运行中 !!!",
        "status_paused": "程序已暂停",
        "status_picking": "移动到目标位置！",
        "hotkey_lbl": "快捷键:",
        "hotkey_btn": "更改按键",
        "hotkey_cancel": "取消更改",
        "hotkey_msg": "请按任意键...",
        "grp_pos": "坐标设置",
        "chk_fixed": "固定坐标",
        "btn_pick": "获取位置 (1秒)",
        "pick_wait": "{}秒后记录...",
        "grp_click": "点击设置",
        "lbl_btn": "按键:",
        "lbl_speed": "间隔(秒):",
        "grp_random": "随机延迟",
        "chk_random": "启用随机",
        "lbl_add": "最大增加(秒):",
        "chk_top": "窗口置顶",
        "btn_pause": "暂停程序",
        "btn_resume": "恢复程序",
        "tip_pick": "1秒后获取坐标。\n请移动到目标位置。",
        "tip_speed": "请输入数字 (如: 0.1)\n无效时默认为0.1",
        "tip_random": "请输入数字"
    }
}

# --- 설정 파일 관리 ---
class ConfigManager:
    def __init__(self, filename="resd_settings.json"):
        self.filename = filename
        self.default_config = {
            "language": "Auto",
            "speed": "0.1",
            "random_enabled": False,
            "random_max": "0.1",
            "click_button": "Left",
            "topmost": False,
            "hotkey": "F8",
            "fixed_pos_enabled": False,
            "fixed_x": "0",
            "fixed_y": "0",
            "geometry": None
        }

    def load(self):
        if not os.path.exists(self.filename): return self.default_config
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                for k, v in self.default_config.items():
                    if k not in data: data[k] = v
                return data
        except: return self.default_config

    def save(self, data):
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except: pass

# --- 툴팁 클래스 ---
class ToolTip:
    def __init__(self, widget, text_key, lang_var):
        self.widget = widget
        self.text_key = text_key
        self.lang_var = lang_var
        self.tip_window = None
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tip_window: return
        lang = self.lang_var.get()
        text = LANG_DATA[lang].get(self.text_key, "")
        if not text: return

        x, y, _, _ = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + self.widget.winfo_rooty() + 25
        
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.attributes("-topmost", True)
        tw.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(tw, text=text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("Malgun Gothic", 9))
        label.pack(ipadx=2)

    def hide_tip(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None

# --- 메인 앱 ---
class ModernAutoClicker:
    def __init__(self, root):
        self.root = root
        
        # 설정 로드
        self.config_mgr = ConfigManager()
        self.config = self.config_mgr.load()
        
        # 창 위치 불러오기
        saved_geo = self.config.get("geometry")
        if saved_geo:
            try:
                self.root.geometry(saved_geo)
            except:
                self.root.geometry("420x600")
        else:
            self.root.geometry("420x600")

        self.root.resizable(False, False)
        self.root.configure(bg="white")

        # 언어 감지
        self.current_lang = tk.StringVar()
        saved_lang = self.config.get("language", "Auto")
        if saved_lang == "Auto":
            sys_lang = locale.getdefaultlocale()[0]
            if sys_lang and "ko" in sys_lang.lower(): self.current_lang.set("한국어")
            elif sys_lang and "ja" in sys_lang.lower(): self.current_lang.set("日本語")
            elif sys_lang and "zh" in sys_lang.lower(): self.current_lang.set("中文")
            else: self.current_lang.set("English")
        else:
            self.current_lang.set(saved_lang)

        # 변수 초기화
        self.running = False
        self.program_running = True
        self.global_paused = False
        self.mouse = Controller()
        self.is_setting_key = False
        self.current_hotkey_name = self.config.get("hotkey", "F8")
        self.current_hotkey = self.parse_key_string(self.current_hotkey_name)

        self.var_speed = tk.StringVar(value=self.config.get("speed", "0.1"))
        self.var_random_enabled = tk.BooleanVar(value=self.config.get("random_enabled", False))
        self.var_random_max = tk.StringVar(value=self.config.get("random_max", "0.1"))
        self.var_click_btn = tk.StringVar(value=self.config.get("click_button", "Left"))
        self.var_topmost = tk.BooleanVar(value=self.config.get("topmost", False))
        self.var_fixed_enabled = tk.BooleanVar(value=self.config.get("fixed_pos_enabled", False))
        self.var_fixed_x = tk.StringVar(value=self.config.get("fixed_x", "0"))
        self.var_fixed_y = tk.StringVar(value=self.config.get("fixed_y", "0"))

        # --- 스타일 설정 ---
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background="white")
        style.configure("TLabel", background="white", font=("Malgun Gothic", 10))
        style.configure("TButton", font=("Malgun Gothic", 9))
        style.configure("TCheckbutton", background="white", font=("Malgun Gothic", 10))
        style.configure("TLabelframe", background="white")
        style.configure("TLabelframe.Label", background="white", font=("Malgun Gothic", 10, "bold"), foreground="#4a90e2")
        
        style.map('TCombobox', 
                  fieldbackground=[('readonly', 'white')], 
                  selectbackground=[('readonly', 'white')], 
                  selectforeground=[('readonly', 'black')])
        
        style.configure("TCombobox", 
                        arrowsize=12,
                        background="white",
                        arrowcolor="#555555",
                        relief="flat",
                        borderwidth=1,
                        padding=5)

        self.create_widgets()
        self.apply_language()
        self.apply_topmost()
        self.start_threads()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_widgets(self):
        # 1. 헤더
        header_frame = tk.Frame(self.root, bg="white")
        header_frame.pack(fill="x", padx=10, pady=5)
        self.cb_lang = ttk.Combobox(header_frame, textvariable=self.current_lang, 
                                    values=["한국어", "English", "日本語", "中文"], 
                                    state="readonly", width=10)
        self.cb_lang.pack(side="right")
        self.cb_lang.bind("<<ComboboxSelected>>", self.apply_language)

        # 2. 상태 표시
        self.status_frame = tk.Frame(self.root, bg="white", pady=10)
        self.status_frame.pack(fill="x")
        self.lbl_status = tk.Label(self.status_frame, text="STATUS", 
                                   font=("Malgun Gothic", 18, "bold"), bg="white", fg="#555555")
        self.lbl_status.pack()
        
        # 3. 단축키
        self.hotkey_frame = tk.Frame(self.root, bg="#f0f5fa", pady=10)
        self.hotkey_frame.pack(fill="x", padx=10, pady=5)
        self.lbl_hotkey_title = tk.Label(self.hotkey_frame, text="Hotkey:", bg="#f0f5fa", font=("Malgun Gothic", 10))
        self.lbl_hotkey_title.pack(side="left", padx=10)
        self.lbl_hotkey_val = tk.Label(self.hotkey_frame, text=self.current_hotkey_name, bg="#f0f5fa", font=("Malgun Gothic", 11, "bold"), fg="#4a90e2")
        self.lbl_hotkey_val.pack(side="left")
        self.btn_hotkey = tk.Button(self.hotkey_frame, text="Change", command=self.enable_hotkey_setting, 
                                    relief="flat", bg="white", bd=1)
        self.btn_hotkey.pack(side="right", padx=10)

        # 4. 좌표 설정
        self.grp_pos = ttk.LabelFrame(self.root, text="Position", padding=10)
        self.grp_pos.pack(fill="x", padx=10, pady=5)
        self.chk_fixed = ttk.Checkbutton(self.grp_pos, text="Fixed Pos", variable=self.var_fixed_enabled)
        self.chk_fixed.pack(anchor="w")
        
        f_coord = tk.Frame(self.grp_pos, bg="white")
        f_coord.pack(fill="x", pady=5)
        tk.Label(f_coord, text="X:", bg="white").pack(side="left")
        
        tk.Entry(f_coord, textvariable=self.var_fixed_x, width=6, relief="solid", bd=1).pack(side="left", padx=2)
        
        tk.Label(f_coord, text="Y:", bg="white").pack(side="left", padx=5)
        tk.Entry(f_coord, textvariable=self.var_fixed_y, width=6, relief="solid", bd=1).pack(side="left", padx=2)
        
        self.btn_pick = tk.Button(f_coord, text="Pick (1s)", command=self.pick_location_countdown, 
                                  bg="#e1e1e1", relief="flat", font=("Malgun Gothic", 8))
        self.btn_pick.pack(side="right")
        ToolTip(self.btn_pick, "tip_pick", self.current_lang)

        # 5. 클릭/속도
        self.grp_click = ttk.LabelFrame(self.root, text="Click Settings", padding=10)
        self.grp_click.pack(fill="x", padx=10, pady=5)
        f_c1 = tk.Frame(self.grp_click, bg="white")
        f_c1.pack(fill="x", pady=2)
        self.lbl_btn = tk.Label(f_c1, text="Button:", bg="white")
        self.lbl_btn.pack(side="left")
        self.cb_btn = ttk.Combobox(f_c1, textvariable=self.var_click_btn, values=["Left", "Right"], state="readonly", width=8)
        self.cb_btn.pack(side="right")
        
        self.cb_btn.bind("<<ComboboxSelected>>", lambda e: self.root.focus_set())

        f_c2 = tk.Frame(self.grp_click, bg="white")
        f_c2.pack(fill="x", pady=2)
        self.lbl_speed = tk.Label(f_c2, text="Speed:", bg="white")
        self.lbl_speed.pack(side="left")
        
        self.ent_speed = tk.Entry(f_c2, textvariable=self.var_speed, width=8, relief="solid", bd=1)
        self.ent_speed.pack(side="right")
        ToolTip(self.ent_speed, "tip_speed", self.current_lang)

        # 6. 랜덤
        self.grp_random = ttk.LabelFrame(self.root, text="Random", padding=10)
        self.grp_random.pack(fill="x", padx=10, pady=5)
        self.chk_random = ttk.Checkbutton(self.grp_random, text="Enable Random", variable=self.var_random_enabled)
        self.chk_random.pack(anchor="w")
        f_rnd = tk.Frame(self.grp_random, bg="white")
        f_rnd.pack(fill="x", pady=2)
        self.lbl_add = tk.Label(f_rnd, text="Add:", bg="white")
        self.lbl_add.pack(side="left")
        
        self.ent_random = tk.Entry(f_rnd, textvariable=self.var_random_max, width=8, relief="solid", bd=1)
        self.ent_random.pack(side="right")
        ToolTip(self.ent_random, "tip_random", self.current_lang)

        # 7. 하단 설정
        self.frame_bottom = tk.Frame(self.root, bg="white")
        self.frame_bottom.pack(side="bottom", pady=20, fill="x", padx=20)
        
        self.chk_top = ttk.Checkbutton(self.frame_bottom, text="Always Top", variable=self.var_topmost, command=self.apply_topmost)
        self.chk_top.pack(side="top", pady=(0, 15))
        
        self.btn_pause = tk.Button(self.frame_bottom, text="Pause Program", command=self.toggle_global_pause, 
                                   bg="#ffdddd", font=("Malgun Gothic", 11, "bold"), 
                                   relief="flat")
        self.btn_pause.pack(fill="x", ipady=5)

    def apply_language(self, event=None):
        if event:
             self.root.focus_set()
             
        lang = self.current_lang.get()
        data = LANG_DATA[lang]
        
        # [수정] 버전 정보(APP_VERSION)를 제목에 함께 표시
        self.root.title(f"{data['title']} ({APP_VERSION})")
        
        self.update_status_text()
        
        self.lbl_hotkey_title.config(text=data["hotkey_lbl"])
        if self.is_setting_key:
            self.btn_hotkey.config(text=data["hotkey_cancel"])
        else:
            self.btn_hotkey.config(text=data["hotkey_btn"])

        self.grp_pos.config(text=data["grp_pos"])
        self.chk_fixed.config(text=data["chk_fixed"])
        if "1" in self.btn_pick.cget("text") or "Pick" in self.btn_pick.cget("text") or "위치" in self.btn_pick.cget("text") or "位置" in self.btn_pick.cget("text"):
             self.btn_pick.config(text=data["btn_pick"])

        self.grp_click.config(text=data["grp_click"])
        self.lbl_btn.config(text=data["lbl_btn"])
        self.lbl_speed.config(text=data["lbl_speed"])
        self.grp_random.config(text=data["grp_random"])
        self.chk_random.config(text=data["chk_random"])
        self.lbl_add.config(text=data["lbl_add"])
        self.chk_top.config(text=data["chk_top"])
        
        if self.global_paused:
            self.btn_pause.config(text=data["btn_resume"], bg="#ddffdd")
        else:
            self.btn_pause.config(text=data["btn_pause"], bg="#ffdddd")

    def update_status_text(self):
        lang = self.current_lang.get()
        if self.global_paused:
            self.lbl_status.config(text=LANG_DATA[lang]["status_paused"], fg="#e67e22")
            return

        if self.running:
            self.lbl_status.config(text=LANG_DATA[lang]["status_run"], fg="#e74c3c")
        else:
            self.lbl_status.config(text=LANG_DATA[lang]["status_wait"], fg="#2ecc71")
            if self.is_setting_key:
                 self.lbl_status.config(text=LANG_DATA[lang]["hotkey_msg"], fg="#3498db")

    def toggle_global_pause(self):
        self.global_paused = not self.global_paused
        if self.global_paused:
            self.running = False
        self.apply_language()
        self.update_status_text()

    def pick_location_countdown(self):
        self.btn_pick.config(state="disabled")
        lang = self.current_lang.get()
        self.lbl_status.config(text=LANG_DATA[lang]["status_picking"], fg="#9b59b6")
        self.countdown(1)

    def countdown(self, count):
        lang = self.current_lang.get()
        if count > 0:
            msg = LANG_DATA[lang]["pick_wait"].format(count)
            self.btn_pick.config(text=msg)
            self.root.after(1000, lambda: self.countdown(count - 1))
        else:
            x, y = self.mouse.position
            self.var_fixed_x.set(str(x))
            self.var_fixed_y.set(str(y))
            self.btn_pick.config(text=LANG_DATA[lang]["btn_pick"], state="normal")
            self.update_status_text()

    def enable_hotkey_setting(self):
        if self.is_setting_key:
            self.is_setting_key = False
            self.apply_language()
            self.update_status_text()
        else:
            self.is_setting_key = True
            self.apply_language()
            self.update_status_text()

    def parse_key_string(self, key_str):
        try:
            if len(key_str) == 1: return keyboard.KeyCode(char=key_str)
            else: return getattr(keyboard.Key, key_str.lower())
        except: return keyboard.Key.f8

    def get_key_name(self, key):
        try:
            if hasattr(key, 'char') and key.char: return key.char.upper()
            else: return str(key).replace("Key.", "").upper()
        except: return "Unknown"

    def apply_topmost(self):
        self.root.attributes("-topmost", self.var_topmost.get())

    def on_press(self, key):
        if self.global_paused:
            return

        if self.is_setting_key:
            self.current_hotkey = key
            self.current_hotkey_name = self.get_key_name(key)
            self.lbl_hotkey_val.config(text=self.current_hotkey_name)
            self.is_setting_key = False
            self.apply_language()
            self.update_status_text()
            return

        if key == self.current_hotkey:
            self.running = not self.running
            self.update_status_text()

    def clicker(self):
        while self.program_running:
            if self.global_paused:
                time.sleep(0.2)
                continue

            if self.running:
                if self.var_fixed_enabled.get():
                    try:
                        fx = int(self.var_fixed_x.get())
                        fy = int(self.var_fixed_y.get())
                        self.mouse.position = (fx, fy)
                    except ValueError:
                        pass 

                btn_str = self.var_click_btn.get()
                btn = Button.right if btn_str == "Right" else Button.left
                self.mouse.click(btn)
                
                try:
                    base = float(self.var_speed.get())
                except ValueError:
                    base = 0.1

                if self.var_random_enabled.get():
                    try:
                        rnd_max = float(self.var_random_max.get())
                    except ValueError:
                        rnd_max = 0.1
                    add = random.uniform(0, rnd_max)
                    time.sleep(base + add)
                else:
                    time.sleep(base)
            else:
                time.sleep(0.01)

    def start_threads(self):
        t = threading.Thread(target=self.clicker)
        t.daemon = True
        t.start()
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def on_close(self):
        data = {
            "language": self.current_lang.get(),
            "speed": self.var_speed.get(),
            "random_enabled": self.var_random_enabled.get(),
            "random_max": self.var_random_max.get(),
            "click_button": self.var_click_btn.get(),
            "topmost": self.var_topmost.get(),
            "hotkey": self.current_hotkey_name,
            "fixed_pos_enabled": self.var_fixed_enabled.get(),
            "fixed_x": self.var_fixed_x.get(),
            "fixed_y": self.var_fixed_y.get(),
            "geometry": self.root.geometry()
        }
        self.config_mgr.save(data)
        self.program_running = False
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernAutoClicker(root)
    root.mainloop()