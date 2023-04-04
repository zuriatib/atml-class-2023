

###
###
### NOTE:
### This is not a sample solution and some computations might be wrong!
###
###




import matplotlib.pyplot as plt
import numpy as np

from stackjackClass import StackJack, ACTION_STAND, ACTION_STACK_1, ACTION_STACK_2


### Define constants etc.

# Point where the player goes bust.
# We use this index to encode the terminal state
# (even if the player decided to stand).
BUST = 27

# "Cost" of drawing a card
REWARD_CARD = -1

# Rewards for the different outcomes
REWARD_WIN = 10
REWARD_DRAW = 0
REWARD_LOST = -10
REWARD_BUST = -20

# Stacks that cards are drawn from
STACK1 = list(range(1, 6))
STACK2 = list(range(11, 16))
DEALER_STACK = list(range(20, 27))

# List of possible states
STATES = list(range(BUST + 1))

# List of possible actions
ACTIONS = [ACTION_STAND, ACTION_STACK_1, ACTION_STACK_2]

# Choose a small threshold
THETA = 1e-15

# No discounting necessary -> gamma is 1
GAMMA = 1






# Evaluate the policy that always chooses "stand"
print('Evaluate policy "stand"')

# Initialize values at 0
# We use one extra slot for the terminal state after going bust
values = np.zeros(BUST + 1)

while True:
    Delta = 0
    # We do not need to update the terminal state (BUST)
    # Iterate over all other states
    for s in range(BUST):
        # Remember old value
        v = values[s]

        # Compute expected reward for action "stand"
        newValue = 0
        for dc in DEALER_STACK:
            if s > dc:
                reward = REWARD_WIN
            elif s == dc:
                reward = REWARD_DRAW
            else:
                reward = REWARD_LOST
            # We can ignore the new state value since it is always the terminal one (=0)
            newValue += 1/len(DEALER_STACK) * reward
        
        # update values, Delta
        Delta = max(Delta, abs(v - newValue))
        values[s] = newValue

    # stop if no significant change:
    print(Delta)
    if Delta < THETA:
        break

valuesStand = values.copy()

print(valuesStand)







# Evaluate the policy that always chooses "stack 0"
print('Evaluate policy "stack 0"')

# Initialize values at 0
# We use one extra slot for the terminal state after going bust
values = np.zeros(BUST + 1)

while True:
    Delta = 0
    # We do not need to update the terminal state (BUST)
    # Iterate over all other states
    for s in range(BUST):
        # Remember old value
        v = values[s]

        # Compute expected reward for action "stack 0"
        newValue = 0
        for card in STACK1:
            newSum = s + card
            if newSum >= BUST:
                newValue += 1/len(STACK1) * (REWARD_BUST + REWARD_CARD)
            else:
                newValue += 1/len(STACK1) * (GAMMA * values[newSum] + REWARD_CARD)
        
        # update values, Delta
        Delta = max(Delta, abs(v - newValue))
        values[s] = newValue

    # stop if no significant change:
    print(Delta)
    if Delta < THETA:
        break

valuesStack1 = values.copy()

print(valuesStack1)







# Evaluate the policy that randomly chooses an action with probabilities:
print('Evaluate policy "random"')
P_STAND = 0.3
P_STACK0 = 0.5
P_STACK1 = 0.2

# Initialize values at 0
# We use one extra slot for the terminal state after going bust
values = np.zeros(BUST + 1)

while True:
    Delta = 0
    # We do not need to update the terminal state (BUST)
    # Iterate over all other states
    for s in range(BUST):
        # Remember old value
        v = values[s]

        # Compute value of each action separately, then combine with probabilities
        # Compute expected reward for action "stack 0"
        newValueStack0 = 0
        for card in STACK1:
            newSum = s + card
            if newSum >= BUST:
                newValueStack0 += 1/len(STACK1) * (REWARD_BUST + REWARD_CARD)
            else:
                newValueStack0 += 1/len(STACK1) * (GAMMA * values[newSum] + REWARD_CARD)

        # Compute expected reward for action "stack 1"
        newValueStack1 = 0
        for card in STACK2:
            newSum = s + card
            if newSum >= BUST:
                newValueStack1 += 1/len(STACK2) * (REWARD_BUST + REWARD_CARD)
            else:
                newValueStack1 += 1/len(STACK2) * (GAMMA * values[newSum] + REWARD_CARD)
        
        # Compute expected reward for action "stand"
        newValueStand = 0
        for dc in DEALER_STACK:
            if s > dc:
                reward = REWARD_WIN
            elif s == dc:
                reward = REWARD_DRAW
            else:
                reward = REWARD_LOST
            # We can ignore the new state value since it is always the terminal one (=0)
            newValueStand += 1/len(DEALER_STACK) * reward
        
        # Compute new value after choosing randomly
        newValue = (
            P_STAND * newValueStand
            + P_STACK0 * newValueStack0
            + P_STACK1 * newValueStack1
        )
        
        # update values, Delta
        Delta = max(Delta, abs(v - newValue))
        values[s] = newValue

    # stop if no significant change:
    print(Delta)
    if Delta < THETA:
        break

valuesRandom = values.copy()
print(valuesRandom)






### Find optimal policy
print('Find optimal policy')

# Initialize values at 0
# We use one extra slot for the terminal state after going bust
values = np.zeros(BUST + 1)
policyInds = [0] * BUST

while True:
    Delta = 0
    # We do not need to update the terminal state (BUST)
    # Iterate over all other states
    for s in range(BUST):
        # Remember old value
        v = values[s]

        # Compute value of each action separately, then choose maximum value
        # Compute expected reward for action "stack 0"
        newValueStack0 = 0
        for card in STACK1:
            newSum = s + card
            if newSum >= BUST:
                newValueStack0 += 1/len(STACK1) * (REWARD_BUST + REWARD_CARD)
            else:
                newValueStack0 += 1/len(STACK1) * (GAMMA * values[newSum] + REWARD_CARD)

        # Compute expected reward for action "stack 1"
        newValueStack1 = 0
        for card in STACK2:
            newSum = s + card
            if newSum >= BUST:
                newValueStack1 += 1/len(STACK2) * (REWARD_BUST + REWARD_CARD)
            else:
                newValueStack1 += 1/len(STACK2) * (GAMMA * values[newSum] + REWARD_CARD)
        
        # Compute expected reward for action "stand"
        newValueStand = 0
        for dc in DEALER_STACK:
            if s > dc:
                reward = REWARD_WIN
            elif s == dc:
                reward = REWARD_DRAW
            else:
                reward = REWARD_LOST
            # We can ignore the new state value since it is always the terminal one (=0)
            newValueStand += 1/len(DEALER_STACK) * reward
        
        # Compute new value after choosing randomly
        candidateValues = [newValueStand, newValueStack0, newValueStack1]
        ind = np.argmax(candidateValues)
        policyInds[s] = ind
        newValue = candidateValues[ind]
        
        # update values, Delta
        Delta = max(Delta, abs(v - newValue))
        values[s] = newValue

    # stop if no significant change:
    print(Delta)
    if Delta < THETA:
        break


policyOptimal = [ACTIONS[i] for i in policyInds]
valuesOptimal = values.copy()

print(valuesOptimal)
print(policyOptimal)





### Verify values with Monte-Carlo

def evalPolicy(s0=0, n=100, p=[1, 0, 0], plot=False):
    allRewards = []
    for i in range(n):
        allRewards.append(playOneGame(s0, p))
    # tv = tv / n
    if plot:
        plt.hist(allRewards)
        plt.show()
    return np.mean(allRewards)

def playOneGame(s0=0, policy=[1,0,0]):
    sj = StackJack()
    if len(policy) == 3:
        policy = [policy for s in sj.STATES]
    sj.state = s0
    value = 0
    gammaPow = 1
    while True:
        a = np.random.choice(ACTIONS, p=policy[sj.state])
        (reward, state) = sj.step(a)
        value += gammaPow * reward
        gammaPow *= GAMMA
        if state == sj.BUST:
            break
    return value

s0 = 11
ret = evalPolicy(s0, 100, [P_STAND, P_STACK0, P_STACK1])
print(ret)
print(valuesRandom[s0])

policyOptimal2 = []
for selA in policyOptimal:
    tmp = [1*(selA == a) for a in ACTIONS]
    policyOptimal2.append(tmp)


ret = evalPolicy(s0, 10000, policyOptimal2, False)

print(ret)
print(valuesOptimal[s0])

