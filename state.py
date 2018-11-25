import copy


class State():

    def __init__(self):
        self.pinns = [[], [], []]
        self.bottomDisc = [pinn[0] for pinn in self.pinns if len(pinn) == 2]

    def StringToState(self, str):
        self.str = str
        bottom = self.str[0]
        top = self.str[2]
        self.pinns[int(self.str[1]) - 1].extend(bottom)
        self.pinns[int(self.str[3]) - 1].append(top)
        self.bottomDisc = [pinn[0] for pinn in self.pinns if len(pinn) == 2]

    def ListToString(self):
        try:
            bn = str(self.pinns.index(['b']) + 1)
            sn = str(self.pinns.index(['s']) + 1)
            self.str = 'b' + bn + 's' + sn
        except ValueError:
            for idx, pinn in enumerate(self.pinns):
                if len(pinn) == 2:
                    temp = ''.join(pinn)
                    final = temp[0] + str(idx + 1) + temp[1] + str(idx + 1)
            self.str = final


    def SetPinns(self, pinns):
        self.pinns = pinns
        self.bottomDisc = [pinn[0] for pinn in self.pinns if len(pinn) == 2]


    def AllPossbileMoves(self):

        self.possibleMoves = []

        for move in AllMoves:

            if move[0] not in self.bottomDisc and move not in self.str:

                self.possibleMoves.append(move)

        if self.pinns == [[],[],['b','s']]:

            self.possibleMoves = ''

        return self.possibleMoves

    def MakeMistake(self, targetmove):

        for move in self.possibleMoves:

            if move[0] == targetmove[0]:

                if move[1] != targetmove[1]:

                    return move

    def GetReward(self):
        if self.bottomDisc == ['s']:
            self.reward = -10
        elif self.pinns == [[], [], ['b', 's']]:
            self.reward = 100
        else:
            self.reward = -1
        return self.reward


    def GetEndState(self, move):

        try:

            if move in self.AllPossbileMoves():

                idx = next(idx for idx, val in enumerate(self.pinns) if move[0] in val)

                newPinns = copy.deepcopy(self.pinns)

                popped = newPinns[idx].pop()

                newPinns[int(move[1]) - 1].append(popped)

                newState = State()
                newState.SetPinns(newPinns)
                newState.ListToString()

                return newState

        except TypeError:

                newState = State()
                newState.pinns = copy.deepcopy(self.pinns)

                return newState

    def __eq__(self, other):
        return self.str == other.str

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.str)

    def __iter__(self):
        return self


AllMoves = ["s1", "s2", "s3", "b1", "b2", "b3"]
