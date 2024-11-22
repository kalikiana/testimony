# SPDX-FileCopyrightText: 2024 Liv Dywan <liv.dywan@suse.com>
#
# SPDX-License-Identifier: EUPL-1.2

from . import job

import tensorflow as tf
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.models import load_model
from tensorflow.keras import layers, losses
import numpy as np

class Model:
    jobs: str

    def __init__(self, jobs: str):
        self.jobs = jobs

        self.filename = 'openqa_classifier.h5'
        self.max_sequence_length = 500
        self.max_features = 10000
        
        try:
            model = load_model(self.filename)
        except FileNotFoundError:
            embedding_dim = 16
            model = tf.keras.Sequential([
                layers.Embedding(self.max_features, embedding_dim),
                layers.Dropout(0.2),
                layers.GlobalAveragePooling1D(),
                layers.Dropout(0.2),
                layers.Dense(1, activation='sigmoid')])
        self.model = model

    def train(self) -> {}:
        print(f"Training {self.jobs}")
        for uri in self.jobs:
            job.Job(uri).fetch()

        dataset = tf.keras.utils.text_dataset_from_directory('dataset')
        max_squence_length = 500
        vectorize_layer = layers.TextVectorization(
            max_tokens=self.max_features, output_mode='int',
            output_sequence_length=self.max_sequence_length)
        train_text = dataset.map(lambda x, y: x)
        vectorize_layer.adapt(train_text)

        def vectorize_text(text, label):
            text = tf.expand_dims(text, -1)
            return vectorize_layer(text), label

        train_dataset = dataset.map(vectorize_text).cache().prefetch(buffer_size=tf.data.AUTOTUNE)
        self.model.compile(
            loss=losses.BinaryCrossentropy(),
            optimizer='adam',
            metrics=[tf.metrics.BinaryAccuracy(threshold=0.5)])
        history = self.model.fit(train_dataset, epochs=10)

        self.model.save(self.filename)
        print(self.model.summary())
