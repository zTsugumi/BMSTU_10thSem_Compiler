import graphviz

class Automata:
  def __init__(self, alphabet = set(['0', '1'])):
    self.states = set()
    self.alphabet = alphabet
    self.transitions = dict()
    self.init_state = None
    self.final_states = []
  
  @staticmethod
  def epsilon():
    return 'ɛ'

  def set_init_state(self, state):
    self.init_state = state
    self.states.add(state)

  def add_final_states(self, states):
    if isinstance(states, int):
      states = [states]
    for state in states:
      if state not in self.final_states:
        self.final_states.append(state)
  
  def add_transition(self, src_state, dst_state, label):
    '''
      Add a transition (src, dst, label) to transition table
      Args:
        src_state:
        dst_state:
        label:
    '''
    if isinstance(label, str):
      label = set([label])

    self.states.add(src_state)
    self.states.add(dst_state)

    if src_state in self.transitions:
      if dst_state in self.transitions[src_state]:
        self.transitions[src_state][dst_state] = self.transitions[src_state][dst_state].union(label)
      else:
        self.transitions[src_state][dst_state] = label
    else:
      self.transitions[src_state] = {dst_state: label}

  def add_transition_dict(self, transitions):
    '''
      Add a given list of transitions to the transition table
      Args:
        transitions:         
    '''
    for src_state, dst_states in transitions.items():
      for dst_state in dst_states:
        self.add_transition(src_state, dst_state, dst_states[dst_state])
  
  def get_transitions(self, states, label):
    '''
      Get transition states from a list of source states
    '''
    if isinstance(states, int):
      states = [states]

    dst_states = set()
    for src_state in states:
      if src_state in self.transitions:
        for dst_state in self.transitions[src_state]:
          if label in self.transitions[src_state][dst_state]:
            dst_states.add(dst_state)
    
    return dst_states
  
  def get_inv_transitions(self, states, label):
    '''
      Get inverse transition states of a given state
    '''
    if isinstance(states, int):
      states = [states]

    src_states = set()
    for dst_state in states:
      for src_state, dst_states in self.transitions.items():
        if dst_state in dst_states and label in self.transitions[src_state][dst_state]:
          src_states.add(src_state)
    
    return src_states

  def get_eps_closure(self, inp_state):
    '''
      Get the epsilon-closure of a given input state
      Args:
        src_state: int / list of int
    '''
    eclosure = set()
    available = set([inp_state])

    while available:
      src_state = available.pop()
      eclosure.add(src_state)
      if src_state in self.transitions:
        for dst_state in self.transitions[src_state]:
          labels = self.transitions[src_state][dst_state]
          if Automata.epsilon() in labels and dst_state not in eclosure:
            available.add(dst_state)

    return eclosure

  def rebuild_from_number(self, num):
    translations = {}
    for state in list(self.states):
      translations[state] = num
      num += 1

    rebuild = Automata(self.alphabet)

    rebuild.set_init_state(translations[self.init_state])
    rebuild.add_final_states(translations[self.final_states[0]])

    for src_state, dst_states in self.transitions.items():
      for dst_state in dst_states:
        label = dst_states[dst_state]
        rebuild.add_transition(
          translations[src_state], translations[dst_state], label)
    
    return [rebuild, num]

  def rebuild_from_equivalent(self, pos):
    rebuild = Automata(self.alphabet)

    rebuild.set_init_state(pos[self.init_state])
    for s in self.final_states:
      rebuild.add_final_states(pos[s])

    for src_state, dst_states in self.transitions.items():
      for dst_state in dst_states:
        label = dst_states[dst_state]
        rebuild.add_transition(pos[src_state], pos[dst_state], label)

    return rebuild

  def display(self, path=None):
    if path is not None:
      with open(path, 'w') as f:
        print(f'States: {self.states}', file=f)
        print(f'Init state: {self.init_state}', file=f)
        print(f'Final states: {self.final_states}', file=f)
        print(f'Transitions:', file=f)
        for src_state, dst_states in self.transitions.items():
          for dst_state in dst_states:
            for label in dst_states[dst_state]:
              print(f'\t{src_state} --> {dst_state} on {label}', file=f)
          print(file=f)
    else:
      print(f'States: {self.states}')
      print(f'Init state: {self.init_state}')
      print(f'Final states: {self.final_states}')
      print(f'Transitions:')
      for src_state, dst_states in self.transitions.items():
        for dst_state in dst_states:
          for label in dst_states[dst_state]:
            print(f'\t{src_state} --> {dst_state} on {label}')
        print()
  
  def drawGraph(self, path):
    dot = graphviz.Digraph(graph_attr={'rankdir': 'LR', 'root': 's1'})

    if self.states:
      dot.node('start', '', shape='point')
      dot.edge('start', f's{self.init_state}')

      for state in self.states:
        if state in self.final_states:
          dot.node(f's{state}', f's{state}', shape='doublecircle')
        else:
          dot.node(f's{state}', f's{state}', shape='circle')
      
      for src_state, dst_states in self.transitions.items():
        for dst_state in dst_states:
          for label in dst_states[dst_state]:
            dot.edge(f's{src_state}', f's{dst_state}', label)    

    dot.render(path, view=True)

class BuildAutomata:
  '''
    Class for building epsilon-NFA basic structures
  '''
  @staticmethod
  def epsilon():
    state1 = 1
    state2 = 2
    epsilon = Automata()
    epsilon.set_init_state(state1)
    epsilon.add_final_states(state2)
    epsilon.add_transition(state1, state2, Automata.epsilon())
    return epsilon

  @staticmethod
  def basic(label):
    state1 = 1
    state2 = 2
    basic = Automata()
    basic.set_init_state(state1)
    basic.add_final_states(state2)
    basic.add_transition(state1, state2, label)
    return basic
  
  @staticmethod
  def plus(a, b):
    [a, m1] = a.rebuild_from_number(2)
    [b, m2] = b.rebuild_from_number(m1)
    state1 = 1
    state2 = m2
    plus = Automata()
    plus.set_init_state(state1)
    plus.add_final_states(state2)
    plus.add_transition(plus.init_state, a.init_state, Automata.epsilon())
    plus.add_transition(plus.init_state, b.init_state, Automata.epsilon())
    plus.add_transition(a.final_states[0], plus.final_states[0], Automata.epsilon())
    plus.add_transition(b.final_states[0], plus.final_states[0], Automata.epsilon())
    plus.add_transition_dict(a.transitions)
    plus.add_transition_dict(b.transitions)
    return plus

  @staticmethod
  def dot(a, b):
    [a, m1] = a.rebuild_from_number(1)
    [b, m2] = b.rebuild_from_number(m1)
    state1 = 1
    state2 = m2 - 1
    dot = Automata()
    dot.set_init_state(state1)
    dot.add_final_states(state2)
    dot.add_transition(a.final_states[0], b.init_state, Automata.epsilon())    
    dot.add_transition_dict(a.transitions)
    dot.add_transition_dict(b.transitions)
    return dot

  @staticmethod
  def star(a):
    [a, m1] = a.rebuild_from_number(2)    
    state1 = 1
    state2 = m1
    star = Automata()
    star.set_init_state(state1)
    star.add_final_states(state2)
    star.add_transition(star.init_state, a.init_state, Automata.epsilon())
    star.add_transition(star.init_state, star.final_states[0], Automata.epsilon())
    star.add_transition(a.final_states[0], star.final_states[0], Automata.epsilon())
    star.add_transition(a.final_states[0], a.init_state, Automata.epsilon())    
    star.add_transition_dict(a.transitions)    
    return star
