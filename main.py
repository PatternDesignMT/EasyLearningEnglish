name: Flet Build APK

on:
  push:
    branches: [ main, master ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pandas "flet[all]"

      - name: Setup Java
        uses: actions/setup-java@v4
        with:
          distribution: 'zulu'
          java-version: '17'

      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        with:
          channel: 'stable'

      - name: Build APK
        run: |
          # Lisansları onayla
          yes | flutter doctor --android-licenses || true
          # SADECE BU KOMUT: Flet otomatik olarak main.py'yi bulacak
          flet build apk --verbose

      - name: Upload APK
        if: success()
        uses: actions/upload-artifact@v4
        with:
          name: EasyLearningEnglish-App
          path: build/apk/*.apk
