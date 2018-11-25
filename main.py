from state import State
import random

# Initializing variables
errorProb = 0.1
rightProb = 1 - errorProb
GAMMA = 0.9
AllMoves = ["s1", "s2", "s3", "b1", "b2", "b3"]  # All possible moves
statestrings = ["b1s1", "b1s2", "b1s3", "s2b2", "s3b3", "b3s2",
                "b2s3", "b3s3", "b2s2", "b3s1", "b2s1", "s1b1"]  # All possbile states


# Initializing List of State Objects
def InitializeStates():
    States = []
    for i, str in enumerate(statestrings):
        States.append(State())
        States[i].StringToState(str)
        States[i].AllPossbileMoves()
        States[i].GetReward()
    return States


States = InitializeStates()
values = dict.fromkeys(States, 0)  # Initializing Value Dictionary

"""
Calculate Value Algorithm 
Inputs: - State Object
        - Action
        - Dictionary of Values for each state
Outputs: Expected value for this State - Action
"""

# Calculating value for a particular state
def CalculateValue(state, move):
    try:
        rightMove = move
        errorMove = state.MakeMistake(move)

        rightEndState = state.GetEndState(rightMove)
        errorEndState = state.GetEndState(errorMove)

        expReward = rightEndState.GetReward() * rightProb \
                    + errorEndState.GetReward() * errorProb

        expValue = values[rightEndState] * rightProb \
                   + values[errorEndState] * errorProb

        new = expReward + GAMMA * expValue
        return new
    except:
        return 0;

"""
Value Iteration Algorithm. 
Inputs: - List of State objects
        - error threshold
Outputs: Tuple containing 
        Optimal Policy dictionary for each state
        Optimal Value dictionary for each state
"""

def ValueIteration(States, error):
    delta = 1
    policies = dict.fromkeys(States, 0)
    while delta > error:

        delta = 0

        tempValues = [0] * len(States)

        for n, state in enumerate(States):
            policie_aux = []
            new = [0] * len(state.possibleMoves)

            for i, move in enumerate(state.possibleMoves):

                # Calculating expected rewards
                new[i] = CalculateValue(state, move)
                policie_aux.append(move)

            try:
                tempValues[n] = max(new)
                policy = policie_aux[new.index(tempValues[n])]
                policies[state] = policy
            except ValueError:
                tempValues[n] = 0
                policies[state] = ''

        if abs(tempValues[n] - values[state]) > delta:
            delta = abs(tempValues[n] - values[state])

        for n, i in enumerate(values):
            values[i] = tempValues[n]

    print("-----------------------------------------------------------")
    print("Results in Value Iteration")
    print("- - - - - - - - - - - - - ")
    [print("For state", i.str,'optimal policy is', policies[i],'values is', round(values[i], 2)) for i in values]
    print()

    return values, policies


ValueIteration(States, 0.001)

"""
Policy Iteration Algorithm. 
Inputs: - List of State objects
Outputs: Tuple containing 
        Optimal Policy dictionary for each state
"""

def PolicyIteration(States):
    policies = dict.fromkeys(States, '')
    utilities = dict.fromkeys(States, '')
    values = dict.fromkeys(States, 0)

    # Assigning random policies for each state. Catching the exception for the absorbing State
    for state in States:
        try:
            policies[state] = random.choice(state.AllPossbileMoves())
        except IndexError:
            policies[state] = ''

    unchanged = False
    iteration = 0
    while not unchanged:

        unchanged = True

        # Calculating values for each state given policy
        for state in States:
            try:
                values[state] = CalculateValue(state, policies[state])
            except IndexError:
                values[state] = 0

        # Iterate over states to get the optimal policy
        for state in States:
            policie_aux = []
            new = [0] * len(state.possibleMoves)

            # Calculating expected rewards and values
            for i, move in enumerate(state.AllPossbileMoves()):
                new[i] = CalculateValue(state, move)
                policie_aux.append(move)


            try:
                maxvalue = max(new)
                policy = policie_aux[new.index(maxvalue)]
            except ValueError:
                maxvalue = 0
                policy = ''

            # Try to update "Unchanged"
            if policies[state] != policy:
                policies[state] = policy
                utilities[state] = maxvalue
                unchanged = False
            elif iteration == 0:
                utilities[state] = maxvalue

        iteration = iteration + 1

    print("-----------------------------------------------------------")
    print("Results in Policy Iteration")
    print("- - - - - - - - - - - - - ")
    [print("For state", i.str, 'optimal policy is', policies[i], 'value is', round(utilities[i], 2))  for i in policies]
    return policies

PolicyIteration(States)


def check_error_policy_value(times):
    V_Aux = {}
    for x in range(1, times):
        (values, policies) = ValueIteration(States, 0.001)
        # print(PolicyIteration(States))
        for key, value in PolicyIteration(States).items():
            if not (policies[key] == value):
                try:
                    V_Aux[key] = V_Aux[key] + 1
                except KeyError:
                    V_Aux[key] = 1

    if (len(V_Aux) == 0):
        print("There are no errors, both iterations have the same result")
    else:
        for key, value in V_Aux.items():
            print("For state " + key.str + " there have been " + V_Aux[key])


# check_error_policy_value(1000)
