from utils.querier import querier
import copy
import numpy
import math


no_query_keys = ['number', 'register:way', 'job_description']

# All possible intents (for one-hot conversion in ST.get_state())
all_intents = ['inform', 'request', 'done', 'thanks']

# All possible slots (for one-hot conversion in ST.get_state())
all_slots = ['name', 'time:start', 'time:end', 'place', 'benefit:ctxh', 'benefit:drl', 'benefit:others',
             'contact', 'host', 'job_description', 'number', 'register:time:start',
             'register:time:end', 'register:way', 'requirement']


class StateTracker:
    """Tracks the state of the episode/conversation and prepares the state representation for the agent."""

    def __init__(self):
        self.db_helper = querier.Querier()
        # self.match_key = usersim_default_key
        self.intents_dict = convert_list_to_dict(all_intents)
        self.num_intents = len(all_intents)
        self.slots_dict = convert_list_to_dict(all_slots)
        self.num_slots = len(all_slots)
        self.max_round_num = 10
        self.none_state = numpy.zeros(self.get_state_size())
        self.current_informs = {}
        self.user_requests = []
        self.cur_action = {}
        self.answer = {}
        self.history = []
        self.last_agent_request = None
        self.reset()

    def get_state_size(self):
        """Returns the state size of the state representation used by the agent."""

        return 2 * self.num_intents + 8 * self.num_slots + 4 + self.max_round_num

    def reset(self):
        """Resets current_informs, history, round_num and user_requests"""

        self.current_informs = {}
        # A list of the dialogues (dicts) by the agent and user so far in the conversation
        # self.history = []
        self.round_num = 0
        # self.user_requests = []
        self.cur_action = {}
        self.answer = {}

    def reset_user_requests(self):
        self.user_requests = []

    def print_history(self):
        """Helper function if you want to see the current history action by action."""

        for action in self.history:
            print(action)

    def get_state(self, done=False):
        """
        Returns the state representation as a numpy array which is fed into the agent's neural network.

        The state representation contains useful information for the agent about the current state of the conversation.
        Processes by the agent to be fed into the neural network. Ripe for experimentation and optimization.

        Parameters:
            done (bool): Indicates whether this is the last dialogue in the episode/conversation. Default: False

        Returns:
            numpy.array: A numpy array of shape (state size,)

        """

        # If done then fill state with zeros
        # print(self.current_informs)
        # print(self.slots_dict)
        if done:
            return self.none_state

        user_action = self.history[-1]
        db_results_dict = self.db_helper.get_db_results_for_slots(self.current_informs)
        filtered_db_results_dict = self.db_helper.get_db_results_for_slots(self.current_informs, is_filter=True)
        print('DB ', db_results_dict)
        print('DB Filter', filtered_db_results_dict)
        if filtered_db_results_dict['matching_all_constraints'] == 0:
            return None

        last_agent_action = self.history[-2] if len(self.history) > 1 else None
        if last_agent_action and 'intent' in last_agent_action.keys():
            if last_agent_action['intent'] in ['greeting', 'complete', 'activities']:
                last_agent_action['intent'] = 'done'

        # Create one-hot of intents to represent the current user action
        user_act_rep = numpy.zeros((self.num_intents,))
        
        # Sang adjust code here ###############
        # if user_action['intent'] == 'complete':
        #     user_action.update({'intent': 'thanks'})

        user_act_rep[self.intents_dict[user_action['intent']]] = 1.0

        # Create bag of inform slots representation to represent the current user action
        user_inform_slots_rep = numpy.zeros((self.num_slots,))
        for key in user_action['inform_slots'].keys():
            user_inform_slots_rep[self.slots_dict[key]] = 1.0

        # Create bag of request slots representation to represent the current user action
        user_request_slots_rep = numpy.zeros((self.num_slots,))
        for key in user_action['request_slots'].keys():
            sub_keys = get_sub_keys(key)
            for sub_key in sub_keys:
                user_request_slots_rep[self.slots_dict[sub_key]] = 1.0

        # Create bag of filled_in slots based on the current_slots
        current_slots_rep = numpy.zeros((self.num_slots,))
        for key in self.current_informs:
            current_slots_rep[self.slots_dict[key]] = 1.0

        # Encode last agent intent
        agent_act_rep = numpy.zeros((self.num_intents,))
        if last_agent_action:
            agent_act_rep[self.intents_dict[last_agent_action['intent']]] = 1.0

        # Encode last agent inform slots
        agent_inform_slots_rep = numpy.zeros((self.num_slots,))
        if last_agent_action:
            for key in last_agent_action['inform_slots'].keys():
                agent_inform_slots_rep[self.slots_dict[key]] = 1.0

        # Encode last agent request slots
        agent_request_slots_rep = numpy.zeros((self.num_slots,))
        if last_agent_action:
            for key in last_agent_action['request_slots'].keys():
                sub_keys = get_sub_keys(key)
                for sub_key in sub_keys:
                    user_request_slots_rep[self.slots_dict[sub_key]] = 1.0

        # Value representation of the round num
        turn_rep = numpy.zeros((1,)) + self.round_num

        # One-hot representation of the round num
        turn_onehot_rep = numpy.zeros((self.max_round_num,))
        turn_onehot_rep[self.round_num - 1] = 1.0

        # Representation of DB query results (scaled counts)
        kb_count_rep = numpy.zeros((self.num_slots + 1,))
        for key in db_results_dict.keys():
            if key in self.slots_dict:
                kb_count_rep[self.slots_dict[key]] = self.normalize_number_query_doc(db_results_dict[key])
        kb_count_rep[-1] = self.normalize_number_query_doc(db_results_dict['matching_all_constraints'])

        # Representation of DB query results (after filtering by score).
        kb_count_rep_filtered = numpy.zeros((self.num_slots + 1,))
        for key in filtered_db_results_dict.keys():
            if key in self.slots_dict:
                kb_count_rep_filtered[self.slots_dict[key]] = self.normalize_number_query_doc(filtered_db_results_dict[key])
        kb_count_rep_filtered[-1] = self.normalize_number_query_doc(filtered_db_results_dict['matching_all_constraints'])

        # Representation of DB query results (binary)
        kb_binary_rep = numpy.zeros((self.num_slots + 1,))
        for key in db_results_dict.keys():
            if key in self.slots_dict:
                kb_binary_rep[self.slots_dict[key]] = numpy.sum(db_results_dict[key] > 0.)
        kb_binary_rep[-1] = numpy.sum(db_results_dict['matching_all_constraints']> 0.)
        
        state_representation = numpy.hstack(
            [user_act_rep, user_inform_slots_rep, user_request_slots_rep, agent_act_rep, agent_inform_slots_rep,
             agent_request_slots_rep, current_slots_rep, turn_rep, turn_onehot_rep, kb_count_rep, kb_count_rep_filtered, kb_binary_rep]).flatten()
        
        # print(state_representation)
        print('LENGTH ', len(state_representation))

        return state_representation

    def update_state_agent(self, agent_action):
        """
        Updates the dialogue history with the agent's action and augments the agent's action.

        Takes an agent action and updates the history. Also augments the agent_action param with query information and
        any other necessary information.

        Parameters:
            agent_action (dict): The agent action of format dict('intent': string, 'inform_slots': dict,
                                 'request_slots': dict) and changed to dict('intent': '', 'inform_slots': {},
                                 'request_slots': {}, 'round': int, 'speaker': 'Agent')

        """
        if agent_action['intent'] == 'inform':
            assert agent_action['inform_slots']
            inform_slots = self.db_helper.fill_inform_slot(agent_action['inform_slots'], self.current_informs)
            agent_action['inform_slots'] = inform_slots
            assert agent_action['inform_slots']
            items = list(agent_action['inform_slots'].items())
            for item in items:
                key = item[0]
                value = item[1]
                assert key != 'match_found'
                assert value != 'PLACEHOLDER', 'KEY: {}'.format(key)
                if value != 'not match available':
                    self.current_informs[key] = value
        # If intent is match_found then fill the action informs with the matches informs (if there is a match)
        elif agent_action['intent'] == 'match_found':
            assert not agent_action['inform_slots'], 'Cannot inform and have intent of match found!'
            db_results = self.db_helper.get_db_results(self.current_informs)
            if db_results:
                # Arbitrarily pick the first value of the dict
                items = list(db_results.items())[0]
                agent_action['inform_slots'] = copy.deepcopy(value)
                # agent_action['inform_slots'][self.match_key] = str(key)
            # else:
                # agent_action['inform_slots'][self.match_key] = 'no match available'
            # self.current_informs[self.match_key] = agent_action['inform_slots'][self.match_key]
        
        elif agent_action['intent'] == 'request':
            self.set_last_agent_request(list(agent_action['request_slots'])[0])

        agent_action.update({'round': self.round_num, 'speaker': 'Agent'})
        self.history.append(agent_action)
        self.set_cur_action(agent_action)

    def update_state_user(self, user_action):
        """
        Updates the dialogue history with the user's action and augments the user's action.

        Takes a user action and updates the history. Also augments the user_action param with necessary information.

        Parameters:
            user_action (dict): The user action of format dict('intent': string, 'inform_slots': dict,
                                 'request_slots': dict) and changed to dict('intent': '', 'inform_slots': {},
                                 'request_slots': {}, 'round': int, 'speaker': 'User')

        """

        for key, value in user_action['inform_slots'].items():
            self.current_informs[key] = value
        user_action.update({'round': self.round_num, 'speaker': 'User'})
        self.history.append(user_action)
        self.round_num += 1
        self.set_cur_action(user_action)

    def add_user_requests(self, request):
        self.user_requests.append(request)

    def remove_user_requests(self, request = None):
        if request is None:
            self.user_requests = []
            return
        
        self.user_requests = list(filter(lambda val: list(val.keys())[0] != request, self.user_requests))

    def get_first_user_request(self):
        if len(self.user_requests) == 0:
            return
        
        return self.user_requests[0]
    
    def set_cur_action(self, action):
        self.cur_action = action

    def get_cur_action(self):
        return self.cur_action
    
    def set_answer(self, text = None):
        self.answer = self.cur_action
        if text is not None:
            self.answer = text

    def get_answer(self):
        return self.answer
    
    def reset_answer(self):
        self.answer = {}

    def reset_current_informs(self):
        self.current_informs = {}

    def set_last_agent_request(self, request):
        self.last_agent_request = request

    def reset_last_agent_request(self):
        self.last_agent_request = None

    def get_activities(self):
        return self.db_helper.get_all_activities(self.current_informs)
    
    def normalize_number_query_doc(self, num_of_docs):
        return (1./(1. + math.exp(-(num_of_docs-5)/1.8)))


def convert_list_to_dict(lst):
    if len(lst) > len(set(lst)):
        raise ValueError('List must be unique!')
    return {k: v for v, k in enumerate(lst)}

def get_sub_keys(key):
    sub_keys = []
    if key == 'time':
        sub_keys = ['time:start', 'time:end']
    elif key == 'register:time':
        sub_keys = ['register:time:start', 'register:time:end']
    elif key == 'benefit':
        sub_keys = ['benefit:drl', 'benefit:ctxh', 'benefit:others']
    else:
        sub_keys = [key]

    return sub_keys
