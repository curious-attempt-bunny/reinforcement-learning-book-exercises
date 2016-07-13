# setup: pip install matplotlib
# python3 <this file>

import matplotlib.pyplot as plt
import numpy as np

np.random.seed(1234) # make experiments repeatable

# q_star - the true mean rewards for each of the 10 actions
q_star = np.random.rand(10) * 4 - 2 # random in the range -2 to 2

# returns the reward for taking a given action (see figure 2.1 on page 30)
def bandit(action):
  mean = q_star[action]
  stdev = 1.0
  reward = np.random.normal(mean, stdev) # gaussian distribution
  return reward

# Algorithm comes from page 33 of https://www.dropbox.com/s/b3psxv2r0ccmf80/book2015oct.pdf?dl=0
def execute_steps(total_steps, epsilon = 0.1):
  Q = np.zeros(np.size(q_star)) # initial estimates are zero
  N = np.zeros(np.size(q_star))

  reward = np.zeros(total_steps)
  optimal = np.zeros(total_steps)

  for step in range(total_steps):
    if np.random.rand() >= epsilon:
      # exploit

      # this resolves tie breaks randomly (otherwise np.argmax(Q) would be simpler)
      A = np.random.choice(np.where(Q == Q.max())[0])
    else:
      # explore
      A = np.random.randint(np.size(q_star))

    R = bandit(A)
    N[A] += 1
    Q[A] += (1.0/N[A])*(R-Q[A])

    if A == np.argmax(q_star):
      optimal[step] = 1

    reward[step] = R

  # debug information to get a feel for how it works (try altering the size of q_star and epsilon)
  # print(q_star)
  # print(Q)
  # print(N)
  # print(np.argmax(q_star))
  # print(np.argmax(Q))

  return reward, optimal

# uncomment the lines below for the longer calculation that parameter searches for epsilon

epsilons = np.array([0.0, 0.01, 0.1])
#epsilons = np.array([0.0, 0.01, 0.1, 1.0/128, 1.0/64, 1.0/32, 1.0/16, 1.0/8, 1.0/4])

average_reward = np.zeros([1000, np.size(epsilons)])
average_optimal = np.zeros([1000, np.size(epsilons)])
averages = np.zeros(np.size(epsilons))
number_of_tasks = 2000

print('|'*int((np.size(epsilons)*number_of_tasks)/100))
for idx, epsilon in enumerate(epsilons):
  for task in range(number_of_tasks):
    reward, optimal = execute_steps(1000, epsilon = epsilon)
    average_reward[:,idx] += reward
    average_optimal[:,idx] += optimal
    # averages[idx] += np.mean(reward)
    if task % 100 == 99:
      print('.', end="", flush=True)

  average_reward[:,idx] /= number_of_tasks
  average_optimal[:,idx] /= number_of_tasks
  # averages[idx] /= number_of_tasks

fig, ax = plt.subplots(3, figsize=[12, 8])
for idx in range(np.size(epsilons)):
  ax[0].plot(average_reward[:,idx], label='epsilon = {}'.format(epsilons[idx]))
ax[0].set_xlabel('Steps')
ax[0].set_ylabel('Average reward')
ax[0].legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)

for idx in range(np.size(epsilons)):
  ax[1].plot(average_optimal[:,idx])
ax[1].set_xlabel('Steps')
ax[1].set_ylabel('% Optimal action')

# ax[2].plot(averages[3:])
# ax[2].set_xlabel('Epsilons: {}'.format(epsilons[3:]))
# ax[2].set_ylabel('Average reward over first 1000 steps')

plt.show()