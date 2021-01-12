"""Module housing GAN for fake comment creation."""

from tensorflow.keras.activations import ReLU
from tensorflow.keras.layers import (LSTM, Bidirectional, Dense, Flatten,
                                     TimeDistributed)
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.optimizers import Adam


class FakeCommentator:
    """GAN for creationg fake_comments."""

    def __init__(self) -> None:
        """Initialize FakeCommentator."""
        # Declare instance variables
        self.generator = None
        self.discriminator = None
        self.gan = None

    def _build_generator(self):
        # Create a sequential model
        generator = Sequential()

        # Add first layer with activation function (TODO: input_shape)
        generator.add(
            Bidirectional(
                LSTM(128, return_sequences=True),
                input_shape=(maxlen, 90)
                )
            )
        generator.add(ReLU())

        # Add more layers
        for _ in range(3):
            generator.add(
                Bidirectional(LSTM(64, return_sequences=True))
                )
            generator.add(ReLU())

        # Add time distibuted layer
        generator.add(TimeDistributed(Dense(64)))
        generator.add(ReLU())

        # Densify
        generator.add(Dense(len(encoding), activation='softmax'))

        # Compile and return model
        optimizer = Adam(lr=0.1)
        generator.compile(
            loss='categorical_crossentropy', optimizer=optimizer
            )

        return generator

    def _build_discriminator(self):
        # Create sequential model
        discriminator = Sequential()

        # Add input layer (TODO: input_shape)
        discriminator.add(Bidirectional(
            LSTM(256, return_sequences=True),
            input_shape=(maxlen, len(encoding))
            ))
        discriminator.add(ReLU())

        # Add time distributed layer
        discriminator.add(TimeDistributed(Dense(256)))
        discriminator.add(ReLU())

        # Add Flatten layer
        discriminator.add(Flatten())
        discriminator.add(ReLU())

        # Add dense layer
        discriminator.add(Dense(1, activation='sigmoid'))

        # Compile and return model
        optimizer = Adam(lr=0.1)
        discriminator.compile(loss='binary_crossentropy', optimizer=optimizer)

        return discriminator

    def _build_gan(self):
        pass

    def train(self):
        """Train the GAN."""
        pass

    def predict(self):
        """Generate fake comments."""
        pass
