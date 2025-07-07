import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt

# MNIST dataset lai load gareko
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

# Data lai normalize gareko
x_train, x_test = x_train / 255.0, x_test / 255.0

# simple neural network model build gareko
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])

# model lai compile gareko
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# model lai train gareko
model.fit(x_train, y_train, epochs=5, validation_data=(x_test, y_test))

# model lai evaluate gareko
test_loss, test_acc = model.evaluate(x_test, y_test)
print(f'Test accuracy: {test_acc:.4f}')

# model lai save gareko
model.save('mnist_digit_model.h5')
print('Model saved as mnist_digit_model.h5')