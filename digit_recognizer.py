import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageGrab
import pytesseract
import os

# Set the path to tesseract.exe if it's not in your PATH
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

DIGIT_NAMES = {
    "0": "zero",
    "1": "one",
    "2": "two",
    "3": "three",
    "4": "four",
    "5": "five",
    "6": "six",
    "7": "seven",
    "8": "eight",
    "9": "nine"
}

class DigitRecognizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Digit Recognizer (OCR)")
        self.canvas_width = 200
        self.canvas_height = 200

        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg='black')
        self.canvas.pack()

        self.button_frame = tk.Frame(root)
        self.button_frame.pack()

        self.recognize_btn = tk.Button(self.button_frame, text="Recognize", command=self.recognize_digit)
        self.recognize_btn.pack(side=tk.LEFT, padx=5)

        self.clear_btn = tk.Button(self.button_frame, text="Clear", command=self.clear_canvas)
        self.clear_btn.pack(side=tk.LEFT, padx=5)

        self.result_label = tk.Label(root, text="", font=("Arial", 20))
        self.result_label.pack(pady=10)

        self.last_x, self.last_y = None, None
        self.canvas.bind('<B1-Motion>', self.draw)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

    def draw(self, event):
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, fill='white', width=10, capstyle=tk.ROUND, smooth=True)
        self.last_x, self.last_y = event.x, event.y

    def reset(self, event):
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        self.canvas.delete("all")
        self.result_label.config(text="")

    def recognize_digit(self):
        # Save canvas to an image
        x = self.root.winfo_rootx() + self.canvas.winfo_x()
        y = self.root.winfo_rooty() + self.canvas.winfo_y()
        x1 = x + self.canvas_width
        y1 = y + self.canvas_height

        # Grab the canvas area
        img = ImageGrab.grab().crop((x, y, x1, y1)).convert('L')
        img = img.point(lambda p: 255 if p > 128 else 0)  # Binarize

        # Use pytesseract to recognize the digit
        custom_config = r'--oem 3 --psm 10 -c tessedit_char_whitelist=0123456789'
        text = pytesseract.image_to_string(img, config=custom_config).strip()

        if text and text[0] in DIGIT_NAMES:
            name = DIGIT_NAMES[text[0]]
            self.result_label.config(text=f"{text[0]} ({name})")
        else:
            self.result_label.config(text="Not recognized")

if __name__ == "__main__":
    root = tk.Tk()
    app = DigitRecognizerApp(root)
    root.mainloop() 