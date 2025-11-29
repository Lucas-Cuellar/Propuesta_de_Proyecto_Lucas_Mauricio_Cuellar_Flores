# model_builder.py
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Dropout, Flatten, Dense
from tensorflow.keras import regularizers
from config import CLASSES

def build_cnn(input_shape):
    """
    Crea la CNN con:
    - Menor capacidad (para evitar memorizar ruido).
    - Regularización L2.
    - Dropout progresivo.
    """
    l2_reg = regularizers.l2(0.001)

    model = Sequential(name=f"CNN_Audio_{len(CLASSES)}class")
    model.add(Input(shape=input_shape))

    model.add(Conv2D(16, (3, 3), activation='relu', padding='same',
                     kernel_regularizer=l2_reg))
    model.add(MaxPooling2D((2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(32, (3, 3), activation='relu', padding='same',
                     kernel_regularizer=l2_reg))
    model.add(MaxPooling2D((2, 2)))
    model.add(Dropout(0.3))

    model.add(Conv2D(64, (3, 3), activation='relu', padding='same',
                     kernel_regularizer=l2_reg))
    model.add(MaxPooling2D((2, 2)))
    model.add(Dropout(0.4))

    model.add(Flatten())
    model.add(Dense(64, activation='relu', kernel_regularizer=l2_reg))
    model.add(Dropout(0.5))

    model.add(Dense(len(CLASSES), activation='softmax'))
    return model
