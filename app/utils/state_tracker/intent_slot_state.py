from app.utils.state_tracker.state_tracker import *


class IntentSlotState:
    def __init__(self, intent, request_slots, inform_slots):
        self.action = {}
        self.action['intent'] = intent
        self.action['request_slots'] = {}
        self.action['inform_slots'] = {}
        if request_slots:
            self.action['request_slots'] = request_slots
        if inform_slots:
            self.action['inform_slots'] = inform_slots

    def update_state_tracker(self, state_tracker: StateTracker):
        pass


class UserInformState(IntentSlotState):
    def __init__(self, intent, request_slots, inform_slots):
        super().__init__(intent, request_slots, inform_slots)

    def update_state_tracker(self, state_tracker: StateTracker):
        user_action = self.action
        request = state_tracker.get_first_user_request()
        if request is not None:
            user_action['request_slots'] = request

        state_tracker.update_state_user(user_action)
        return state_tracker


class UserRequestState(IntentSlotState):
    def __init__(self, intent, request_slots, inform_slots):
        super().__init__(intent, request_slots, inform_slots)

    def update_state_tracker(self, state_tracker: StateTracker):
        user_action = self.action
        if 'name' in state_tracker.current_informs.keys() and 'name' in self.action['inform_slots']:
            if self.action['inform_slots']['name'] != state_tracker.current_informs['name']:
                print(self.action['inform_slots']['name'],
                      state_tracker.current_informs['name'])
                state_tracker.reset_current_informs()

        if len(state_tracker.user_requests) == 0:
            state_tracker.add_user_requests(self.action['request_slots'])

        state_tracker.update_state_user(user_action)
        return state_tracker


class UserCompleteState(IntentSlotState):
    def __init__(self, intent, request_slots, inform_slots):
        super().__init__(intent, request_slots, inform_slots)

    def update_state_tracker(self, state_tracker: StateTracker):
        user_action = self.action
        state_tracker.update_state_user(user_action)
        state_tracker.reset()
        state_tracker.remove_user_requests()
        return state_tracker


class UserDefaultState(IntentSlotState):
    def __init__(self, intent, request_slots, inform_slots):
        super().__init__(intent, request_slots, inform_slots)

    def update_state_tracker(self, state_tracker: StateTracker):
        user_action = self.action
        state_tracker.update_state_user(user_action)
        return state_tracker


class AgentInformState(IntentSlotState):
    def __init__(self, intent, request_slots, inform_slots):
        super().__init__(intent, request_slots, inform_slots)

    def update_state_tracker(self, state_tracker: StateTracker):
        agent_action = self.action
        state_tracker.update_state_agent(agent_action)
        if list(state_tracker.get_first_user_request().keys())[0] in agent_action['inform_slots']:
            state_tracker.set_answer()

        return state_tracker


class AgentRequestState(IntentSlotState):
    def __init__(self, intent, request_slots, inform_slots):
        super().__init__(intent, request_slots, inform_slots)

    def update_state_tracker(self, state_tracker: StateTracker):
        agent_action = self.action
        state_tracker.update_state_agent(agent_action)
        return state_tracker


class AgentDoneState(IntentSlotState):
    def __init__(self, intent, request_slots, inform_slots):
        super().__init__(intent, request_slots, inform_slots)

    def update_state_tracker(self, state_tracker: StateTracker):
        agent_action = self.action
        state_tracker.update_state_agent(agent_action)
        state_tracker.reset()
        state_tracker.remove_user_requests()
        return state_tracker


class AgentDefaultState(IntentSlotState):
    def __init__(self, intent, request_slots, inform_slots):
        super().__init__(intent, request_slots, inform_slots)

    def update_state_tracker(self, state_tracker: StateTracker):
        agent_action = self.action
        state_tracker.update_state_agent(agent_action)
        return state_tracker


class DefaultState(IntentSlotState):
    def __init__(self, intent, request_slots, inform_slots):
        super().__init__(intent, request_slots, inform_slots)

    def update_state_tracker(self, state_tracker: StateTracker):
        agent_action = self.action
        state_tracker.update_state_agent(agent_action)
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
    },
    'default': DefaultState,
}


class IntentSlotStateFactory:
    def get_state_object(self, object, intent, request_slots, intent_slots) -> IntentSlotState:
        if object in intent_slot_state_factory_map.keys():
            if intent in intent_slot_state_factory_map[object].keys():
                return intent_slot_state_factory_map[object][intent](intent, request_slots, intent_slots)

            return intent_slot_state_factory_map[object]['default'](intent, request_slots, intent_slots)

        return intent_slot_state_factory_map['default'](intent, request_slots, intent_slots)


class IntentSlotStateContext:
    def set_state_object(self, object, intent, request_slots, intent_slots):
        self.__state_object = IntentSlotStateFactory().get_state_object(
            object, intent, request_slots, intent_slots)

    def update_state_tracker(self, state_tracker: StateTracker):
        if not self.__state_object:
            return state_tracker

        return self.__state_object.update_state_tracker(state_tracker)
