
import random

ACTION_STAND = 0
ACTION_STACK_1 = 1
ACTION_STACK_2 = 2

class StackJack:
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

    def __init__(self, verbose = False):
        self.state = 0
        self.verbose = verbose

    def reset(self, state = 0):
        self.state = state

    def step(self, action):
        # Return early if we are in a terminal state
        if self.state == self.BUST:
            return 0, self.state

        # Perform an action
        if action == ACTION_STAND:
            return self._stand()
        elif action == ACTION_STACK_1 or action == ACTION_STACK_2:
            return self._draw(action)

        # Raise an error if action is invalid
        raise ValueError('Invalid Action!')

    def _stand(self):
        # Draw a card for the dealer
        dealerCard = random.choice(self.DEALER_STACK)
        self._printUpdate('Dealer card:', dealerCard)
        
        # Check the result
        if self.state < dealerCard:
            reward = self.REWARD_LOST
        elif self.state == dealerCard:
            reward = self.REWARD_DRAW
        else:
            reward = self.REWARD_WIN
        
        # Set state to terminal state and return
        self.state = self.BUST
        return reward, self.state

    def _draw(self, action):
        # Draw a card for the player
        if action == ACTION_STACK_1:
            stack = self.STACK1
        else: # (we checked before that this can only be ACTION_STACK_2)
            stack = self.STACK2
        card = random.choice(stack)
        self._printUpdate('Player card:', card)

        # Update the state and check if we went bust
        self.state += card
        if self.state >= self.BUST:
            self._printUpdate('Bust! (', self.state, ')', sep='')
            self.state = self.BUST
            reward = self.REWARD_BUST + self.REWARD_CARD
        else:
            reward = self.REWARD_CARD
        
        return reward, self.state

    def _printUpdate(self, *values, sep=' ', end='\n'):
        # Print an update if `self.verbose == True`, else do nothing.
        if self.verbose:
            print(*values, sep=sep, end=end)
    
    def play(self):
        # Make this instance print updates
        oldVerbosity = self.verbose
        self.verbose = True

        # Explain the game
        print('Enter 0 to stand, 1 for the first stack, 2 for the second stack.')
        print('Anything else to quit.')
        print('You start with a card sum of 0.')

        # Read input and perform action until the user quits or goes bust
        while self.state != self.BUST:
            s = input('> ')
            try:
                ind = int(s)
                reward, state = self.step(ind)
            except:
                print('Quitting.')
                break
            print('Reward:', reward)
            print('State:', state)
        
        # Reset verbosity
        self.verbose = oldVerbosity


def testStackJack():
    sj = StackJack(verbose=True)
    
    for i in range(12):
        reward, state = sj.step(1)
        print('Reward:', reward)
        print('State:', state)

if __name__ == '__main__':
    testStackJack()
    # sj = StackJack()
    # sj.play()

