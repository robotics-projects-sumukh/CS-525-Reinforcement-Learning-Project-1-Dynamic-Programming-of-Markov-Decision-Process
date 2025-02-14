### MDP Value Iteration and Policy Iteration
### Reference: https://web.stanford.edu/class/cs234/assignment1/index.html 
# Modified By Yanhua Li on 09/09/2022 for gym==0.25.2
# Modified By Yanhua Li on 08/19/2023 for gymnasium==0.29.0
import numpy as np

np.set_printoptions(precision=3)

"""
For policy_evaluation, policy_improvement, policy_iteration and value_iteration,
the parameters P, nS, nA, gamma are defined as follows:

	P: nested dictionary
		From gym.core.Environment
		For each pair of states in [1, nS] and actions in [1, nA], P[state][action] is a
		tuple of the form (probability, nextstate, reward, terminal) where
			- probability: float
				the probability of transitioning from "state" to "nextstate" with "action"
			- nextstate: int
				denotes the state we transition to (in range [0, nS - 1])
			- reward: int
				either 0 or 1, the reward for transitioning from "state" to
				"nextstate" with "action"
			- terminal: bool
			  True when "nextstate" is a terminal state (hole or goal), False otherwise
	nS: int
		number of states in the environment
	nA: int
		number of actions in the environment
	gamma: float
		Discount factor. Number in range [0, 1)
"""

def policy_evaluation(P, nS, nA, policy, gamma=0.9, tol=1e-8):
    """Evaluate the value function from a given policy.

    Parameters:
    ----------
    P, nS, nA, gamma:
        defined at beginning of file
    policy: np.array[nS,nA]
        The policy to evaluate. Maps states to actions.
    tol: float
        Terminate policy evaluation when
            max |value_function(s) - prev_value_function(s)| < tol
    Returns:
    -------
    value_function: np.ndarray[nS]
        The value function of the given policy, where value_function[s] is
        the value of state s
    """
    
    value_function = np.zeros(nS)
    ############################
    # YOUR IMPLEMENTATION HERE #
    while True:
        delta = 0

        for s in range(nS):
            v = value_function[s]
            # above v is the value of state s according to the value function value_function
        
            new_value_state = 0 
            # equivalent to value_function[s] = 0, but not use value_function[s] to avoid the error of type mismatch value_function[s] is of type <class 'numpy.float64'> and new_value_state is of type <class 'int'>
            
            for a in range(nA):
                for prob, next_state, reward, terminal in P[s][a]:
                    new_value_state += policy[s][a] * prob * (reward + gamma * value_function[next_state])
                    # above new_value_state is the value of state s according to the value function value_function

            delta = max(delta, abs(new_value_state - v))
            # above delta is the maximum difference between the old value and the new value

            value_function[s] = new_value_state
            # above value_function[s] is the new value of state s according to the value function value_function

        if delta < tol:
            break
    #                          #
    ############################
    # print(value_function)
    return value_function 


def policy_improvement(P, nS, nA, value_from_policy, gamma=0.9):
    """Given the value function from policy improve the policy.

    Parameters:
    -----------
    P, nS, nA, gamma:
        defined at beginning of file
    value_from_policy: np.ndarray
        The value calculated from the policy
    Returns:
    --------
    new_policy: np.ndarray[nS,nA]
        A 2D array of floats. Each float is the probability of the action
        to take in that state according to the environment dynamics and the 
        given value function.
    """

    new_policy = np.ones([nS, nA]) / nA # policy as a uniform distribution
	############################
	# YOUR IMPLEMENTATION HERE #
    policy_stable = True

    while policy_stable:
        for s in range(nS):
            old_action = np.argmax(new_policy[s])
            # above np.argmax(new_policy[s]) returns the action with the highest probability

            action_values = np.zeros(nA)
            for a in range(nA):
                for prob, next_state, reward, done in P[s][a]:
                    action_values[a] += prob * (reward + gamma * value_from_policy[next_state])
                    # above action_values[a] is the value of the action a in state s according to the value function value_from_policy 

            new_action = np.argmax(action_values)
            # above np.argmax(action_values) returns the action with the highest value

            new_policy[s] = np.eye(nA)[new_action]
            # above np.eye(nA)[new_action] returns a one-hot vector of the action with the highest value

            if abs(old_action - new_action) > 1e-4:
                policy_stable = False
                # if the old action is different from the new action, then the policy is not stable
            else:
                policy_evaluation(P, nS, nA, new_policy, gamma)
    #                          #
	############################
    return new_policy

def policy_iteration(P, nS, nA, policy, gamma=0.9, tol=1e-8):
    """Runs policy iteration.

    You should call the policy_evaluation() and policy_improvement() methods to
    implement this method.

    Parameters
    ----------
    P, nS, nA, gamma:
        defined at beginning of file
    policy: policy to be updated
    tol: float
        tol parameter used in policy_evaluation()
    Returns:
    ----------
    new_policy: np.ndarray[nS,nA]
    V: np.ndarray[nS]
    """
    new_policy = policy.copy()
	############################
	# YOUR IMPLEMENTATION HERE #
    delta = 1
    while delta > tol:
        V = policy_evaluation(P, nS, nA, new_policy, gamma, tol)
        new_policy = policy_improvement(P, nS, nA, V, gamma)
        delta = np.max(np.abs(V - policy_evaluation(P, nS, nA, new_policy, gamma, tol)))
    # summary:
    # 1. evaluate the value function V according to the policy new_policy
    # 2. improve the policy new_policy according to the value function V
    # 3. calculate the difference between the old value function and the new value function
    # 4. if the difference is less than tol, then break the loop
    # 5. otherwise, repeat the above steps
    #                          #
	############################
    return new_policy, V

def value_iteration(P, nS, nA, V, gamma=0.9, tol=1e-8):
    """
    Learn value function and policy by using value iteration method for a given
    gamma and environment.

    Parameters:
    ----------
    P, nS, nA, gamma:
        defined at beginning of file
    V: value to be updated
    tol: float
        Terminate value iteration when
            max |value_function(s) - prev_value_function(s)| < tol
    Returns:
    ----------
    policy_new: np.ndarray[nS,nA]
    V_new: np.ndarray[nS]
    """
    V_new = V.copy()
    policy_new = np.zeros([nS, nA])
    ############################
    # YOUR IMPLEMENTATION HERE #
    delta = 1
    while delta > tol:
        delta = 0
        for s in range(nS):
            v = V_new[s]
            # above v is the value of state s according to the value function V_new

            action_values = np.zeros(nA)
            for a in range(nA):
                for prob, next_state, reward, done in P[s][a]:
                    action_values[a] += prob * (reward + gamma * V_new[next_state])
                    # above action_values[a] is the value of the action a in state s according to the value function V_new

            V_new[s] = np.max(action_values)
            # above V_new[s] is the value of state s according to the value function V_new

            policy_new[s] = np.eye(nA)[np.argmax(action_values)]
            # above np.eye(nA)[np.argmax(action_values)] returns a one-hot vector of the action with the highest value

            delta = max(delta, abs(v - V_new[s]))
            # above delta is the maximum difference between the old value and the new value
    #                          #
    ############################
    return policy_new, V_new

def render_single(env, policy, render = False, n_episodes=100):
    """
    Given a game envrionemnt of gym package, play multiple episodes of the game.
    An episode is over when the returned value for "done" = True.
    At each step, pick an action and collect the reward and new state from the game.

    Parameters:
    ----------
    env: gym.core.Environment
      Environment to play on. Must have nS, nA, and P as attributes.
    policy: np.array of shape [env.nS, env.nA]
      The action to take at a given state
    render: whether or not to render the game(it's slower to render the game)
    n_episodes: the number of episodes to play in the game. 
    Returns:
    ------
    total_rewards: the total number of rewards achieved in the game.
    """
    total_rewards = 0
    for _ in range(n_episodes):
        ob, _ = env.reset() # initialize the episode
        done = False
        while not done: # using "not truncated" as well, when using time_limited wrapper.
            if render:
                env.render() # render the game
            ############################
            # YOUR IMPLEMENTATION HERE #
            action = np.argmax(policy[ob])
            # above np.argmax(policy[ob]) returns the action with the highest probability

            ob, reward, done, truncated, _ = env.step(action)
            done = done or truncated
            total_rewards += reward
            # above total_rewards is the sum of all the rewards
            #                          #
            ############################
            
    return total_rewards