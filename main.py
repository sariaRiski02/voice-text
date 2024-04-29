import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QScrollArea
from PyQt5.QtCore import Qt
import speech_recognition as sr
import pyttsx3
from googletrans import Translator


class SpeechToTextApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Translate bahasa inggris ke bahasa indonesia')
        self.setGeometry(100, 100, 400, 300)  # ukuran jendela
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)  # Pusatkan layout

        # Create title label
        title_label = QLabel('Speech-to-Text')
        title_label.setStyleSheet('font-size: 24px; font-weight: bold;')
        layout.addWidget(title_label)

        # Create record button
        self.record_button = QPushButton('Record Speech')
        self.record_button.setStyleSheet(
            '''
            QPushButton {
                font-size: 18px; 
                background-color: #4CAF50; 
                color: white; 
                border: none; 
                padding: 10px 20px; 
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;  /* Change color on hover */
            }
            QPushButton:pressed {
                background-color: #388e3c;  /* Change color when pressed */
            }
            '''
        )
        self.record_button.clicked.connect(self.record_text)
        layout.addWidget(self.record_button)

        # Create scroll area for output
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        self.output_label = QLabel('')
        self.output_label.setStyleSheet('font-size: 16px;')
        self.output_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.output_label.setStyleSheet('font-size: 16px; padding: 10px;')
        self.output_label.setWordWrap(True)
        self.output_label.setTextInteractionFlags(Qt.TextSelectableByMouse)

        scroll_area.setWidget(self.output_label)

        layout.addWidget(scroll_area)

        self.setLayout(layout)

    def record_text(self):
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.2)
                audio = r.listen(source)
                text = r.recognize_google(audio)
                translated_text = self.translate_text(text)
                self.process_text(translated_text)
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("Terjadi kesalahan yang tidak diketahui")

    def translate_text(self, text):
        translator = Translator()
        translated_text = translator.translate(text, src='en', dest='id').text
        return translated_text

    def process_text(self, text):
        self.output_label.setText(text)
        self.speak_text(text)

    def speak_text(self, text):
        engine = pyttsx3.init()
        engine.setProperty('volume', 0)  # set volume disini
        engine.say(text)
        engine.runAndWait()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SpeechToTextApp()
    window.show()
    sys.exit(app.exec_())
