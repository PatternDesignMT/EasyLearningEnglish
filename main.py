import flet as ft
import csv
import random

def main(page: ft.Page):
    page.title = "Easy Learning English"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    
    # Kelimeleri tutacak liste
    words_db = []

    # Veriyi standart Python csv modülü ile yükle
    try:
        with open("A1_Kelimeler.csv", mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                words_db.append(row)
    except Exception as e:
        return page.add(ft.Text(f"Hata: Veri dosyası okunamadı! {e}"))

    def get_new_word():
        return random.choice(words_db) if words_db else {"Word": "No Data", "Turkish": "Veri Yok"}

    # İlk kelimeyi al
    current_data = get_new_word()
    
    word_text = ft.Text(current_data['Word'], size=40, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900)
    translation_text = ft.Text("", size=30, italic=True, color=ft.Colors.GREEN_700)

    def show_translation(e):
        translation_text.value = current_data['Turkish']
        page.update()

    def next_word(e):
        nonlocal current_data
        current_data = get_new_word()
        word_text.value = current_data['Word']
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
