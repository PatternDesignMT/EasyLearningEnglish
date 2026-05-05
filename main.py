import flet as ft
import pandas as pd
import random

def main(page: ft.Page):
    page.title = "Easy Learning English"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.window_width = 400
    page.window_height = 600

    # Veriyi yükle
    try:
        df = pd.read_csv("A1_Kelimeler.csv")
    except Exception as e:
        return page.add(ft.Text(f"Hata: Veri dosyası bulunamadı! {e}"))

    def get_new_word():
        random_row = df.sample(n=1).iloc[0]
        return random_row['Word'], random_row['Turkish']

    current_word, current_translation = get_new_word()

    word_text = ft.Text(current_word, size=40, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900)
    translation_text = ft.Text("", size=30, italic=True, color=ft.Colors.GREEN_700)

    def show_translation(e):
        translation_text.value = current_translation
        page.update()

    def next_word(e):
        nonlocal current_word, current_translation
        current_word, current_translation = get_new_word()
        word_text.value = current_word
        translation_text.value = ""
        page.update()

    page.add(
        ft.Column(
            [
                ft.Text("İngilizce Öğreniyorum", size=20, color=ft.Colors.GREY_700),
                ft.Divider(),
                ft.Container(height=50),
                word_text,
                translation_text,
                ft.Container(height=50),
                ft.ElevatedButton("Anlamını Gör", on_click=show_translation, width=200),
                ft.OutlinedButton("Sıradaki Kelime", on_click=next_word, width=200),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

ft.app(target=main)
