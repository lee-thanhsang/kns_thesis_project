from utils.state_tracker.state_tracker import *


class IntentSlotState:
    def __init__(self, request_slots, inform_slots):
        self.request_slots = request_slots
        self.inform_slots = inform_slots

    def update_state_tracker(self, state_tracker: StateTracker):
        pass

class UserInformState(IntentSlotState):
    def __init__(self, request_slots, inform_slots):
        super().__init__(request_slots, inform_slots)

    def update_state_tracker(self, state_tracker: StateTracker):
        user_action = {}
        user_action['intent'] = 'inform'
        user_action['inform_slots'] = self.inform_slots
        request = state_tracker.get_first_user_request()
        if request is not None:
            user_action['request_slots'] = {request: 'UNK'}
            
        state_tracker.update_state_user(user_action)
        return state_tracker
        

class UserRequestState(IntentSlotState):
    def __init__(self, request_slots, inform_slots):
        super().__init__(request_slots, inform_slots)

    def update_state_tracker(self, state_tracker: StateTracker):
        user_action = {}
        user_action['intent'] = 'request'
        user_action['request_slots'] = self.request_slots
        user_action['inform_slots'] = self.inform_slots
        state_tracker.add_user_requests(self.request_slots)
        state_tracker.update_state_user(user_action)
        return state_tracker
    
class UserCompleteState(IntentSlotState):
    def __init__(self, request_slots, inform_slots):
        super().__init__(request_slots, inform_slots)

    def update_state_tracker(self, state_tracker: StateTracker):
        state_tracker.reset()
        return state_tracker

class UserDefaultState(IntentSlotState):
    def __init__(self, request_slots, inform_slots):
        super().__init__(request_slots, inform_slots)

    def update_state_tracker(self, state_tracker: StateTracker):
        return state_tracker
    
class AgentInformState(IntentSlotState):
    def __init__(self, request_slots, inform_slots):
        super().__init__(request_slots, inform_slots)

    def update_state_tracker(self, state_tracker: StateTracker):
        agent_action = {}
        agent_action['inform_slots'] = self.inform_slots
        agent_action['intent'] = 'inform'
        state_tracker.update_state_agent(agent_action)
        if list(state_tracker.get_first_user_request()['request'].keys())[0] in agent_action['inform_slots']:
            state_tracker.set_answer()
            
        return state_tracker
            
class AgentRequestState(IntentSlotState):
    def __init__(self, request_slots, inform_slots):
        super().__init__(request_slots, inform_slots)

    def update_state_tracker(self, state_tracker: StateTracker):
        agent_action = {}
        agent_action['intent'] = 'request'
        agent_action['inform_slots'] = self.inform_slots
        agent_action['request_slots'] = self.request_slots
        state_tracker.update_state_agent(agent_action)
        return state_tracker

class AgentDefaultState(IntentSlotState):
    def __init__(self, request_slots, inform_slots):
        super().__init__(request_slots, inform_slots)

    def update_state_tracker(self, state_tracker: StateTracker):
        return state_tracker


intent_slot_state_factory_map = {
    'user': {
        'inform': UserInformState,
        'request': UserRequestState,
        'complete': UserCompleteState,
        'default': UserDefaultState,
    },
    'agent': {
        'inform': AgentInformState,
        'request': AgentRequestState,
        'default': AgentDefaultState,
    }
}

class IntentSlotStateFactory:
    def get_state_object(self, object, intent, request_slots, intent_slots) -> IntentSlotState:
        if intent_slot_state_factory_map[object]:
            if intent_slot_state_factory_map[object][intent]:
                return intent_slot_state_factory_map[object][intent](request_slots, intent_slots)
            
            return intent_slot_state_factory_map[object]['default'](request_slots, intent_slots)
        
        return
    
class IntentSlotStateContext:
    def set_state_object(self, object, intent, request_slots, intent_slots):
        self.__state_object = IntentSlotStateFactory().get_state_object(object, intent, request_slots, intent_slots)

    def update_state_tracker(self, state_tracker: StateTracker):
        if not self.__state_object:
            return state_tracker
        
        return self.__state_object.update_state_tracker(state_tracker)
