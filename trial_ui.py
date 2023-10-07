import tkinter as tk
from tkinter import *
from googletrans import Translator, LANGUAGES
import speech_recognition as sr
from gtts import gTTS

translator = Translator()

def detect_language(text):
    detected_language = translator.detect(text)
    return LANGUAGES[detected_language.lang]

def translate_text(text, target_language):
    translated_text = translator.translate(text, dest=target_language).text
    return translated_text

def translate_text_option():
    text = input_text.get("1.0", tk.END).strip()
    
    if text.lower() == 'exit':
        return

    detected_language = detect_language(text)
    detected_language_label.config(text=f"Detected language: {detected_language}")

    target_language = target_language_entry.get()
    translated_text = translate_text(text, target_language)

    output_text.config(state=tk.NORMAL)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, translated_text)
    output_text.config(state=tk.DISABLED)

def translate_audio_option():
    def takecommand():
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Speak the text you want to translate:")
            r.pause_threshold = 1
            audio = r.listen(source)

        try:
            print("Transcribing...")
            transcribed_text = r.recognize_google(audio)
            input_text.delete(1.0, tk.END)
            input_text.insert(tk.END, transcribed_text)
        except Exception as e:
            print("Sorry, couldn't understand. Please try again.")

    takecommand()
    
    detected_language_label.config(text="Detected language:")

def generate_audio(text, output_audio_path):
    tts = gTTS(text, lang='en')
    tts.save(output_audio_path)

def on_record_button_click():
    translate_audio_option()

# GUI Setup

font_tuple = ('Georgia',11)

root = tk.Tk()
root.title("Real-Time Language Translation Tool")

main_frame = tk.Frame(root, padx=20, pady=20,bg="#f9e9ec")
main_frame.pack(expand=True)

# Detected Language
detected_language_label = tk.Label(main_frame, text="Detected language:",font=font_tuple,bg="#f9e9ec")
detected_language_label.grid(row=0, column=0, sticky="w", columnspan=2)

# Input Text
input_label = tk.Label(main_frame, text="Input Text:",font=font_tuple,bg="#f9e9ec")
input_label.grid(row=1, column=0, sticky="w")

input_text = tk.Text(main_frame, height=10, width=50)
input_text.grid(row=2, column=0, columnspan=2, sticky="w")

# Target Language Entry
target_language_label = tk.Label(main_frame, text="Target Language Code:",font=font_tuple,bg="#f9e9ec")
target_language_label.grid(row=3, column=0, sticky="w")

target_language_entry = tk.Entry(main_frame, width=10)
target_language_entry.grid(row=4, column=0, sticky="w")

# Output Text
output_label = tk.Label(main_frame, text="Translated Text:",font=font_tuple,bg="#f9e9ec")
output_label.grid(row=5, column=0, sticky="w")

output_text = tk.Text(main_frame, height=10, width=50, state=tk.DISABLED)
output_text.grid(row=6, column=0, columnspan=2, sticky="w")

# Record Button
record_button = tk.Button(main_frame, text="Record", bg="#ff85a1", command=on_record_button_click,)
record_button.grid(row=7, column=0, pady=30,padx=80, sticky="w")

# Translate Button
translate_button = tk.Button(main_frame, text="Translate", command=translate_text_option,bg="#ff85a1")
translate_button.grid(row=7, column=1, pady=30,padx=80, sticky="e")

root.mainloop()
