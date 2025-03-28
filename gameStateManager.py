class GameStateManager:
    def __init__(self, initialState):
        self.state = initialState
        self.previousState = None

    def get_state(self):
        return self.state
    
    def set_state(self, newState):
        self.previousState = self.state
        self.state = newState

    def getPreviousState(self):
        return self.previousState
        