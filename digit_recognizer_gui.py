import tkinter as tk
from PIL import Image, ImageDraw, ImageOps
import numpy as np
import tensorflow as tf
from tensorflow import keras

# Load the trained model
model = keras.models.load_model('mnist_digit_model.h5')

def center_image(img):
    # Convert to numpy array
    arr = np.array(img)
    # Find bounding box of the digit
    coords = np.column_stack(np.where(arr > 0))
    if coords.size == 0:
        return img
    y0, x0 = coords.min(axis=0)
    y1, x1 = coords.max(axis=0)
    cropped = img.crop((x0, y0, x1+1, y1+1))
    # Create a new blank image and paste the cropped digit in the center
    new_img = Image.new('L', img.size, color=0)
    paste_x = (img.size[0] - cropped.size[0]) // 2
    paste_y = (img.size[1] - cropped.size[1]) // 2
    new_img.paste(cropped, (paste_x, paste_y))
    return new_img

class DigitRecognizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title('Handwritten Digit Recognizer')
        self.canvas_width = 200
        self.canvas_height = 200
        self.bg_color = 'black'
        self.paint_color = 'white'
        self.brush_size = 6  # Thinner brush for better MNIST-like digits

        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg=self.bg_color)
        self.canvas.pack()

        self.button_frame = tk.Frame(root)
        self.button_frame.pack()

        self.recognize_btn = tk.Button(self.button_frame, text='Recognize', command=self.recognize_digit)
        self.recognize_btn.pack(side=tk.LEFT, padx=5)

        self.clear_btn = tk.Button(self.button_frame, text='Clear', command=self.clear_canvas)
        self.clear_btn.pack(side=tk.LEFT, padx=5)

        self.result_label = tk.Label(root, text='', font=('Arial', 20))
        self.result_label.pack(pady=10)

        self.image1 = Image.new('L', (self.canvas_width, self.canvas_height), color=0)
        self.draw = ImageDraw.Draw(self.image1)

        self.last_x, self.last_y = None, None
        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

    def paint(self, event):
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, fill=self.paint_color, width=self.brush_size, capstyle=tk.ROUND, smooth=True)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=255, width=self.brush_size)
        self.last_x, self.last_y = event.x, event.y

    def reset(self, event):
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        self.canvas.delete('all')
        self.draw.rectangle([0, 0, self.canvas_width, self.canvas_height], fill=0)
        self.result_label.config(text='')

    def recognize_digit(self):
        # Resize to 28x28 and invert colors for MNIST
        img = self.image1.copy()
        img = ImageOps.invert(img)
        img = center_image(img)
        img = img.resize((28, 28), Image.LANCZOS)
        img = np.array(img)
        img = 255 - img  # Invert if needed (white digit on black background)
        img = img / 255.0  # Normalize
        img = img.reshape(1, 28, 28)

        # Predict
        pred = model.predict(img)
        digit = np.argmax(pred)
        confidence = np.max(pred)
        self.result_label.config(text=f'Prediction: {digit} (Confidence: {confidence:.2f})')

if __name__ == '__main__':
    root = tk.Tk()
    app = DigitRecognizerGUI(root)
    root.mainloop() 