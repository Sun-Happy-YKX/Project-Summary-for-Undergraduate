
import random
import numpy as np
import os

class ReplayBuffer:
    
    def __init__(self, capacity):
        self.capacity = capacity
        self.buffer = []
        self.position = 0
    
    def push(self, state, action, reward, next_state, done):
        if len(self.buffer) < self.capacity:
            self.buffer.append(None)
        self.buffer[self.position] = [state, action, reward, next_state, done]
        self.position = (self.position + 1) % self.capacity

    # 从buffer中随机选取一个batch的数据
    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        state_batch, action_batch, reward_batch, next_state_batch, done_batch = map(np.stack, zip(*batch))
        return state_batch, action_batch, reward_batch, next_state_batch, done_batch
    
    def __len__(self):
        return len(self.buffer)
    
    def get_mean(self):
        return sum([info[2] for info in self.buffer])/len(self.buffer)
    
    def save(self, saved_dir):
        if not os.path.exists(saved_dir): # 检测是否存在文件夹
            os.makedirs(saved_dir)
        np.save(saved_dir + "/buffer.npy", np.array(self.buffer))
        np.save(saved_dir + "/position.npy", np.array(self.position))
    
    def load(self, saved_dir):
        self.buffer = np.load(saved_dir + "/buffer.npy", allow_pickle=True).tolist()
        print(len(self.buffer))
        self.position = int(np.load(saved_dir + "/position.npy"))