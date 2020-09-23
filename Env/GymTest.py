import gym
from gym import wrappers
import time
env=gym.make('Breakout-v4')
env=wrappers.Monitor(env,'/tmp/cartpole-experiment-1', force=True)
for i_episode in range(20):
        observation=env.reset()
        for t in range(100):
                time.sleep(0.5)
                env.render()
                print(observation)
                action=env.action_space.sample()
                s,r,done,info=env.step(action)
                if done:
                        print("Episode finished after {} timestep".format(t+1))
