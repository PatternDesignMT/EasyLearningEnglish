import flet as ft
import csv
import random

def main(page: ft.Page):
    page.title = "Easy Learning English"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    
    words_db = []

    # Veriyi farklı bir encoding (latin-1) ile okumayı deniyoruz
    # Bu, Türkçe karakter uyuşmazlıklarını genellikle çözer
    try:
        with open("A1_Kelimeler.csv", mode='r', encoding='latin-1') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Sütun isimlerindeki boşlukları temizleyerek listeye ekle
                clean_row = {k.strip(): v.strip() for k, v in row.items()}
                words_db.append(clean_row)
    except Exception as e:
        # Eğer latin-1 de yemezse, hatayı ekranda göster
        return page.add(ft.Text(f"Hata: Veri dosyası okunamadı! {e}"))

    def get_new_word():
        return random.choice(words_db) if words_db else {"Word": "No Data", "Turkish": "Veri Yok"}

    current_data = get_new_word()
    
    word_text = ft.Text(current_data.get('Word', 'Hata'), size=40, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900)
    translation_text = ft.Text("", size=30, italic=True, color=ft.Colors.GREEN_700)

    def show_translation(e):
        translation_text.value = current_data.get('Turkish', 'Veri Yok')
        page.update()

    def next_word(e):
        nonlocal current_data
        current_data = get_new_word()
        word_text.value = current_data.get('Word', 'Hata')
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
