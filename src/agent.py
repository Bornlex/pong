#coding: utf-8


import numpy as np
import random
from tensorflow import keras
from collections import deque
import matplotlib.pyplot as plt

from src.environment import Environment


class Agent(object):
    """
    Implementation of the DQN algorithm.
    """
    def __init__(self, action_space, state_space):
        self.action_space  = action_space
        self.state_space   = state_space
        self.epsilon       = 1
        self.gamma         = 0.95
        self.batch_size    = 64
        self.epsilon_min   = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 1e-3
        self.memory        = deque(maxlen=100000)
        self.model         = self.build_model()
    
    def build_model(self):
        input_x = keras.layers.Input(shape=(self.state_space,))
        x = keras.layers.Dense(64, activation='relu')(input_x)
        x = keras.layers.Dense(64, activation='relu')(x)
        x = keras.layers.Dense(self.action_space, activation='linear')(x)
        model = keras.models.Model(input_x, x)
        model.compile(optimizer=keras.optimizers.Adam(lr=self.learning_rate), loss='mse')
        return model
    
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((
            state,
            action,
            reward,
            next_state,
            done
        ))
    
    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_space)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])
    
    def replay(self):
        if len(self.memory) < self.batch_size:
            return
        minibatch = random.sample(self.memory, self.batch_size)
        states    = np.array([i[0] for i in minibatch])
        actions   = np.array([i[1] for i in minibatch])
        rewards   = np.array([i[2] for i in minibatch])
        n_states  = np.array([i[3] for i in minibatch])
        dones     = np.array([i[4] for i in minibatch])
        states    = np.squeeze(states)
        n_states  = np.squeeze(n_states)
        targets   = rewards + self.gamma * (np.amax(self.model.predict_on_batch(n_states), axis=1)) * (1 - dones)
        targets_full = self.model.predict_on_batch(states)
        indices   = np.array([i for i in range(self.batch_size)])
        targets_full[[indices], [actions]] = targets
        self.model.fit(states, targets_full, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay