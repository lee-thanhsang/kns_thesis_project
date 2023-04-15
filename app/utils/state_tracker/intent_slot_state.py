from utils.state_tracker.state_tracker import *
from fuzzywuzzy import fuzz

MIN_FUZZY_SCORE = 75

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
        user_request = state_tracker.get_first_user_request()
        if user_request is not None:
            user_action['request_slots'] = user_request

        agent_request = state_tracker.last_agent_request
        if agent_request is not None:
            sub_keys = get_sub_keys(agent_request)
            is_exist_key = False
            for sub_key in sub_keys:
                if sub_key in user_action['inform_slots'].keys():
                    is_exist_key = True

            if not is_exist_key:
                for sub_key in sub_keys:
                    if sub_key not in user_action['inform_slots'].keys():
                        user_action['inform_slots'][sub_key] = 'anything'

            state_tracker.reset_last_agent_request()

        state_tracker.update_state_user(user_action)
        return state_tracker


class UserRequestState(IntentSlotState):
    def __init__(self, intent, request_slots, inform_slots):
        super().__init__(intent, request_slots, inform_slots)

    def update_state_tracker(self, state_tracker: StateTracker):
        user_action = self.action
        if 'name' in state_tracker.current_informs.keys() and 'name' in self.action['inform_slots']:
            # [FUTURE_FIX] use fuzzy to compare name between activities.
            print('FUZZY_SCORE', fuzz.ratio(self.action['inform_slots']['name'], state_tracker.current_informs['name']))
            if fuzz.ratio(self.action['inform_slots']['name'], state_tracker.current_informs['name']) < MIN_FUZZY_SCORE:
                print(self.action['inform_slots']['name'],
                      state_tracker.current_informs['name'])
                state_tracker.reset()

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
        if state_tracker.get_first_user_request():
            request_slot = list(state_tracker.get_first_user_request().keys())[0]
            sub_requests = get_sub_keys(request_slot)
            is_answer = False
            for sub_request in sub_requests:
                if sub_request in agent_action['inform_slots']:
                    is_answer = True
                    state_tracker.set_answer()

            if not is_answer:
                print(request_slot, agent_action['inform_slots'])
                state_tracker.set_answer('Wrong decision in model')
                print('wrong decision')

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

class AgentThankState(IntentSlotState):
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
        'thank': AgentThankState,
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
