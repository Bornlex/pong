import matplotlib
matplotlib.use('TkAgg')

import turtle
import numpy as np
import matplotlib.pyplot as plt

from src.environment import Environment
from src.agent import Agent


if __name__ == "__main__":
    environment = Environment()
    agent = Agent(3, 5)
    loss = []
    episode = 1000
    for e in range(episode):
        state = environment.reset()
        state = np.reshape(state, (1, 5))
        score = 0
        max_steps = 1000
        for i in range(max_steps):
            action = agent.act(state)
            reward, next_state, done = environment.step(action)
            score += reward
            next_state = np.reshape(next_state, (1, 5))
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            #agent.replay()
            if done:
                print(f"Episode {e}/{episode}, score: {score}")
                break
        agent.replay()
        loss.append(score)
    plt.plot([i for i in range(episode)], loss)
    plt.xlabel("episodes")
    plt.ylabel("rewards")
    plt.show()