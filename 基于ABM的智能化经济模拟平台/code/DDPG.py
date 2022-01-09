import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import os

from ActorCritic import Actor, Critic
from memory import ReplayBuffer

class DDPG:
    def __init__(self, n_states, n_actions, hidden_dim=90, device="cpu", critic_lr=5e-3,
                 actor_lr=5e-4, gamma=0.99, soft_tau=1e-2, memory_capacity=100000, batch_size=128):
        self.device = device
        self.critic_lr = critic_lr
        self.actor_lr = actor_lr
        self.critic = Critic(n_states, n_actions, hidden_dim).to(device)
        self.actor = Actor(n_states, n_actions, hidden_dim).to(device)
        self.target_critic = Critic(n_states, n_actions, hidden_dim).to(device)
        self.target_actor = Actor(n_states, n_actions, hidden_dim).to(device)

        for target_param, param in zip(self.target_critic.parameters(), self.critic.parameters()):
            target_param.data.copy_(param.data)
        for target_param, param in zip(self.target_actor.parameters(), self.actor.parameters()):
            target_param.data.copy_(param.data)

        self.critic_optimizer = optim.Adam(self.critic.parameters(),  lr=critic_lr)
        self.actor_optimizer = optim.Adam(self.actor.parameters(), lr=actor_lr)
        self.memory = ReplayBuffer(memory_capacity)
        self.batch_size = batch_size
        self.soft_tau = soft_tau
        self.gamma = gamma

    def select_action(self, state):
        state = torch.FloatTensor(state).unsqueeze(0).to(self.device)
        action = self.actor(state)
        # torch.detach()用于切断反向传播
        return action.detach().cpu().numpy()[0]

    def update(self):
        if len(self.memory) < self.batch_size:
            return
        state, action, reward, next_state, done = self.memory.sample(self.batch_size)
        # 将所有变量转为张量
        state = torch.FloatTensor(state).to(self.device)
        next_state = torch.FloatTensor(next_state).to(self.device)
        action = torch.FloatTensor(action).to(self.device)
        reward = torch.FloatTensor(reward).unsqueeze(1).to(self.device)
        done = torch.FloatTensor(np.float32(done)).unsqueeze(1).to(self.device)
        # 注意critic将(s_t,a)作为输入

        actor_loss = self.critic(state, self.actor(state))
        actor_loss = -actor_loss.mean()

        next_action = self.target_actor(next_state)
        target_value = self.target_critic(next_state, next_action.detach())
        expected_value = reward + (1.0 - done) * self.gamma * target_value
        expected_value = torch.clamp(expected_value, -np.inf, np.inf)

        value = self.critic(state, action)
        critic_loss = nn.MSELoss()(value, expected_value.detach())
        
        #训练优化actor及critic网络
        self.actor_optimizer.zero_grad()
        actor_loss.backward()
        self.actor_optimizer.step()

        self.critic_optimizer.zero_grad()
        critic_loss.backward()
        self.critic_optimizer.step()

        # soft更新目标网络
        for target_param, param in zip(self.target_critic.parameters(), self.critic.parameters()):
            target_param.data.copy_(
                target_param.data * (1.0 - self.soft_tau) + param.data * self.soft_tau
            )
        for target_param, param in zip(self.target_actor.parameters(), self.actor.parameters()):
            target_param.data.copy_(
                target_param.data * (1.0 - self.soft_tau) +
                param.data * self.soft_tau
            )
    def save_model(self,path):
        torch.save(self.target_actor.state_dict(), path)

    def load_model(self,path):
        self.actor.load_state_dict(torch.load(path))
    
    def buffer_model_save(self, saved_dir):
        self.memory.save(saved_dir)
        torch.save(self.critic.state_dict(), saved_dir + "/critic_checkpoint.pth")
        torch.save(self.actor.state_dict(), saved_dir + "/actor_checkpoint.pth")
        torch.save(self.target_critic.state_dict(), saved_dir + "/target_critic_checkpoint.pth")
        torch.save(self.target_actor.state_dict(), saved_dir + "/target_actor_checkpoint.pth")
    
    def buffer_model_load(self, saved_dir):
        if not os.path.exists(saved_dir): # 检测是否存在文件夹
            os.makedirs(saved_dir)
            return
        self.memory.load(saved_dir)

        self.critic.load_state_dict(torch.load(saved_dir + "/critic_checkpoint.pth"))
        self.actor.load_state_dict(torch.load(saved_dir + "/actor_checkpoint.pth"))
        self.target_critic.load_state_dict(torch.load(saved_dir + "/target_critic_checkpoint.pth"))
        self.target_actor.load_state_dict(torch.load(saved_dir + "/target_actor_checkpoint.pth"))

        self.critic_optimizer = optim.Adam(
            self.critic.parameters(),  lr=self.critic_lr)
        self.actor_optimizer = optim.Adam(self.actor.parameters(), lr=self.actor_lr)