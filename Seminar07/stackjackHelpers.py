
from stackjackClass import StackJack, ACTION_STAND, ACTION_STACK_1, ACTION_STACK_2

import numpy as np

THETA = 1e-12

GAMMA = 1

def evaluatePolicy(policy):
    values = np.zeros(StackJack.BUST + 1)
    while True:
        delta = 0
        for state in StackJack.STATES:
            oldValue = values[state]
            actionProbabilities = policy[state]
            values[state] = evaluateRandomAction(state, actionProbabilities, values)
            delta = max(delta, abs(values[state] - oldValue))
        
        if delta <= THETA:
            break
    
    return values


def evaluateRandomAction(state, actionProbabilities, currentValues):
    # Return zero if the state is terminal
    if state == StackJack.BUST:
        return 0

    ## Evaluate the "Stand" action
    # After this the game is over/state is terminal -> expected value of next state is 0
    expectedStateValue = 0

    # Start with zero expected reward,
    # then iterate over all cards in the stack and increment.
    expectedReward = 0 # Initialized as zero, incremented below
    for dealerCard in StackJack.DEALER_STACK:
        # Probability of each card is 1/"number of cards"
        pDealerCard = 1/len(StackJack.DEALER_STACK)

        if state > dealerCard:
            expectedReward += pDealerCard * StackJack.REWARD_WIN
        elif state == dealerCard:
            expectedReward += pDealerCard * StackJack.REWARD_DRAW
        else:
            expectedReward += pDealerCard * StackJack.REWARD_LOST
    
    newValueStand = expectedReward + GAMMA * expectedStateValue


    ## Evaluate the "Stack 1" action
    # Start with zero expected reward/state value,
    # then iterate over all cards in the stack and increment.
    expectedStateValue = 0
    expectedReward = 0
    for playerCard in StackJack.STACK1:
        # Probability of each card is 1/"number of cards"
        pPlayerCard = 1/len(StackJack.STACK1)
        newState = min(state + playerCard, StackJack.BUST)
        if newState == StackJack.BUST:
            expectedStateValue += pPlayerCard * 0
            expectedReward += pPlayerCard * (StackJack.REWARD_BUST + StackJack.REWARD_CARD)
        else:
            expectedStateValue += pPlayerCard * currentValues[newState]
            expectedReward += pPlayerCard * StackJack.REWARD_CARD
    newValueStack1 = expectedReward + GAMMA * expectedStateValue


    # Evaluate the "Stack 2" action
    # Start with zero expected reward/state value,
    # then iterate over all cards in the stack and increment.
    expectedStateValue = 0
    expectedReward = 0
    for playerCard in StackJack.STACK2:
        # Probability of each card is 1/"number of cards"
        pPlayerCard = 1/len(StackJack.STACK2)
        newState = min(state + playerCard, StackJack.BUST)
        if newState == StackJack.BUST:
            expectedStateValue += pPlayerCard * 0
            expectedReward += pPlayerCard * (StackJack.REWARD_BUST + StackJack.REWARD_CARD)
        else:
            expectedStateValue += pPlayerCard * currentValues[newState]
            expectedReward += pPlayerCard * StackJack.REWARD_CARD
    newValueStack2 = expectedReward + GAMMA * expectedStateValue

    
    [pStand, pStack1, pStack2] = actionProbabilities
    
    newValue = (
        pStand * newValueStand
        + pStack1 * newValueStack1
        + pStack2 * newValueStack2
    )

    return newValue



# Helper function to evaluate a single (deterministic action)
def evaluateAction(state, action, values):
    actionProbabilites = [0, 0, 0]
    actionProbabilites[action] = 1
    return evaluateRandomAction(state, actionProbabilites, values)


def deterministicToRandomPolicy(detPolicy):
    randomPolicy = []
    for action in detPolicy:
        actionProbabilities = [0, 0, 0]
        actionProbabilities[action] = 1
        randomPolicy.append(actionProbabilities)
    return randomPolicy

def randomToDeterministicPolicy(randomPolicy):
    detPolicy = [np.argmax(probs) for probs in randomPolicy]
    return detPolicy


def chooseGreedyPolicy(values):
    allActions = [ACTION_STAND, ACTION_STACK_1, ACTION_STACK_2]
    policy = []
    for state in StackJack.STATES:
        actionValues = [evaluateAction(state, action, values) for action in allActions]
        
        bestActionIndex = np.argmax(actionValues)
        actionProbabilities = [0 for a in allActions]
        actionProbabilities[bestActionIndex] = 1
        
        policy.append(actionProbabilities)
    
    return policy




