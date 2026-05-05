import ssl
import os
import pandas as pd
import flet as ft
import json
import time
import threading

ssl._create_default_https_context = ssl._create_unverified_context

def main(page: ft.Page):
    page.title = "EasyLearningEnglish"
    page.window_width = 400
    page.window_height = 800
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = "center"
    page.scroll = "adaptive"

    PROGRESS_FILE = "progress.json"

    state = {
        "df": None,
        "index": 0,
        "files": sorted([f for f in os.listdir() if f.endswith(".csv")]),
        "current_file": "",
        "is_playing": False,
        "play_mode": "Kelime + Cümle",
        "delay": 1.5 # Varsayılan süreyi biraz daha seri yaptık
    }

    # UI Bileşenleri
    txt_word = ft.Text("", size=40, weight="bold", color="blue700")
    txt_pron = ft.Text("", size=18, color="grey700", italic=True)
    txt_mean = ft.Text("", size=28, weight="w500", color="green800")
    txt_example = ft.Text("", size=20, text_align="center")
    txt_ex_pron = ft.Text("", size=16, color="grey500")
    txt_ex_mean = ft.Text("", size=18, color="bluegrey400")
    lbl_stats = ft.Text("", size=16, weight="bold")

    def save_progress():
        if state["current_file"]:
            try:
                data = {}
                if os.path.exists(PROGRESS_FILE):
                    with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                        data = json.load(f)
                data[state["current_file"]] = state["index"]
                with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
                    json.dump(data, f)
            except: pass

    def load_progress(file_name):
        try:
            if os.path.exists(PROGRESS_FILE):
                with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get(file_name, 0)
        except: pass
        return 0

    def play_voice(text):
        """Windows ses motoruyla metni seslendirir"""
        clean_text = str(text).replace("'", "").replace('"', "")
        cmd = f'PowerShell -Command "Add-Type –AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\'{clean_text}\')"'
        os.system(cmd)

    def speak_current_logic():
        """Seçili moda göre (Kelime/Cümle/İkisi) seslendirme yapar"""
        if state["df"] is not None:
            row = state["df"].iloc[state["index"]]
            if state["play_mode"] in ["Kelime", "Kelime + Cümle"]:
                play_voice(row["Word"])
            if state["play_mode"] == "Kelime + Cümle":
                time.sleep(0.5) # İkisi arası minik es
            if state["play_mode"] in ["Cümle", "Kelime + Cümle"]:
                play_voice(row["Example Sentence"])

    def autoplay_worker():
        while state["is_playing"]:
            if state["df"] is not None:
                speak_current_logic()
                time.sleep(state["delay"])
                state["index"] = (state["index"] + 1) % len(state["df"])
                update_ui()
            else:
                break

    def toggle_play(e):
        state["is_playing"] = not state["is_playing"]
        btn_play_auto.icon = ft.icons.PAUSE_CIRCLE_FILLED if state["is_playing"] else ft.icons.PLAY_CIRCLE_FILLED
        btn_play_auto.content = ft.Text("Durdur" if state["is_playing"] else "Otomatik Oynat")
        page.update()
        if state["is_playing"]:
            threading.Thread(target=autoplay_worker, daemon=True).start()

    def update_ui():
        if state["df"] is not None:
            row = state["df"].iloc[state["index"]]
            txt_word.value = str(row["Word"])
            txt_pron.value = f"({row['Pronunciation']})"
            txt_mean.value = str(row["Meaning"])
            txt_example.value = str(row["Example Sentence"])
            txt_ex_pron.value = f"({row['Sentence Pronunciation']})"
            txt_ex_mean.value = str(row["Example Meaning"])
            lbl_stats.value = f"{state['index'] + 1} / {len(state['df'])}"
            save_progress()
            page.update()

    def load_data(file_name):
        state["current_file"] = file_name
        try:
            state["df"] = pd.read_csv(file_name, encoding="windows-1254")
        except:
            state["df"] = pd.read_csv(file_name, encoding="utf-8")
        state["index"] = load_progress(file_name)
        update_ui()

    # Dropdownlar
    dd_level = ft.Dropdown(label="Seviye", width=140, options=[ft.dropdown.Option(f) for f in state["files"]], on_change=lambda e: load_data(e.control.value))
    dd_mode = ft.Dropdown(label="Mod", width=140, value="Kelime + Cümle", options=[ft.dropdown.Option("Kelime"), ft.dropdown.Option("Cümle"), ft.dropdown.Option("Kelime + Cümle")], on_change=lambda e: state.update({"play_mode": e.control.value}))
    
    # Bekleme Süresi Menüsü (0.5 - 3.0 sn arası)
    delay_options = []
    i = 0.5
    while i <= 3.0:
        delay_options.append(ft.dropdown.Option(str(i)))
        i += 0.5
    
    dd_delay = ft.Dropdown(label="Bekleme (sn)", width=110, value="1.5", options=delay_options, on_change=lambda e: state.update({"delay": float(e.control.value)}))

    btn_play_auto = ft.ElevatedButton("Otomatik Oynat", icon=ft.icons.PLAY_CIRCLE_FILLED, on_click=toggle_play)

    page.add(
        ft.Column([
            ft.Row([dd_level, dd_mode], alignment="center"),
            dd_delay,
            ft.Container(
                content=ft.Column([
                    txt_word, txt_pron,
                    ft.Divider(height=10, color="transparent"),
                    txt_mean, ft.Divider(height=20),
                    txt_example, txt_ex_pron, txt_ex_mean,
                ], horizontal_alignment="center"),
                padding=20, bgcolor="white", border_radius=20,
            ),
            ft.TextButton(content=lbl_stats, on_click=lambda _: show_word_list(page, state, update_ui)),
            btn_play_auto,
            ft.Row([
                ft.FilledButton("Geri", on_click=lambda _: move_idx(-1)),
                # BURASI DEĞİŞTİ: Artık tek başına kelimeyi değil, seçili modu seslendirir
                ft.FloatingActionButton(icon="play_arrow", on_click=lambda _: speak_current_logic()),
                ft.FilledButton("İleri", on_click=lambda _: move_idx(1)),
            ], alignment="center")
        ], horizontal_alignment="center")
    )

    def move_idx(step):
        if state["df"] is not None:
            state["index"] = (state["index"] + step) % len(state["df"])
            update_ui()

    if state["files"]:
        dd_level.value = state["files"][0]
        load_data(state["files"][0])

def show_word_list(page, state, update_ui):
    def select_word(idx):
        state["index"] = idx
        bs.open = False
        page.update()
        update_ui()
    word_items = [ft.ListTile(title=ft.Text(f"{i+1}. {w}"), on_click=lambda _, i=i: select_word(i)) for i, w in enumerate(state["df"]["Word"])]
    bs = ft.BottomSheet(ft.Container(ft.Column(word_items, scroll="always", height=400), padding=20, bgcolor="white"), open=True)
    page.overlay.append(bs)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
