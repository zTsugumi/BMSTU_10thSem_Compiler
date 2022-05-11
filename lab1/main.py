from automata import Automata, BuildAutomata
from test import test
from easydict import EasyDict
import itertools

class RegexToNFA:
  def __init__(self, regex):
    self.regex = regex
    self.ops = EasyDict({
      'dot': '.',
      'star': '*',
      'plus': '+',
      'openBracket': '(',
      'closeBracket': ')',
    })
    self.permissible_input = [chr(i) for i in range(65,91)]
    self.permissible_input.extend([chr(i) for i in range(97,123)])
    self.permissible_input.extend([chr(i) for i in range(48,58)])
    self.buildNFA()
  
  def buildNFA(self):
    alphabet = set()
    self.stack_ops = []
    self.stack_automata = []
    prev = ":e:"

    if self.regex == '':
      self.stack_automata.append(BuildAutomata.epsilon())

    for char in self.regex:
      # Done
      if char in self.permissible_input:
        alphabet.add(char)
        if prev in self.permissible_input + [self.ops.closeBracket, self.ops.star]:
            self.push_op(self.ops.dot)
        self.stack_automata.append(BuildAutomata.basic(char))

      # Done
      elif char == self.ops.openBracket:
        if prev in self.permissible_input + [self.ops.closeBracket, self.ops.star]:
            self.push_op(self.ops.dot)
        self.stack_ops.append(char)

      # Done
      elif char == self.ops.closeBracket:
        assert prev not in [self.ops.plus, self.ops.dot], f'Error "{char}" after "{prev}"'

        while (1):
          assert len(self.stack_ops) > 0, f'Error "{char}". Empty ops stack'

          op = self.stack_ops.pop()
          if op == self.ops.openBracket:
            break
          elif op in [self.ops.plus, self.ops.dot]:
            self.process_op(op)
      
      # Done
      elif char == self.ops.star:
        assert prev not in [self.ops.plus, self.ops.dot, self.ops.openBracket, self.ops.star], \
          f'Error "{char}" after "{prev}"'
        
        self.process_op(char)

      # Done
      elif char in [self.ops.dot, self.ops.plus]:
        assert prev not in [self.ops.plus, self.ops.dot, self.ops.openBracket], \
          f'Error "{char}" after "{prev}"'

        self.push_op(char)      
      else:
        raise BaseException(f'Symbol {char} is not permissible')
      
      prev = char

    while self.stack_ops:
      op = self.stack_ops.pop()
      self.process_op(op)

    assert len(self.stack_automata) == 1, f'Regex could not be parsed'

    self.nfa = self.stack_automata.pop()
    self.nfa.alphabet = alphabet

  def push_op(self, char):
    while (1):
      if not self.stack_ops or self.stack_ops[-1] == self.ops.openBracket:
        break

      top = self.stack_ops[-1]      

      if top == char or top == self.ops.dot:
        op = self.stack_ops.pop()
        self.process_op(op)
      else:
        break
    self.stack_ops.append(char)
  
  def process_op(self, op):
    assert len(self.stack_automata) > 0, f'Error "{op}". Empty automata stack'

    if op == self.ops.star:
      a = self.stack_automata.pop()
      self.stack_automata.append(BuildAutomata.star(a))
    elif op in [self.ops.plus, self.ops.dot]:
      assert len(self.stack_automata) >= 2, f'Error processing "{op}"'

      a = self.stack_automata.pop()
      b = self.stack_automata.pop()
      if op == self.ops.plus:
        self.stack_automata.append(BuildAutomata.plus(b, a))
      else:
        self.stack_automata.append(BuildAutomata.dot(b, a))

class NFAToDFA:
  def __init__(self, nfa):
    self.buildDFA(nfa)

  def buildDFA(self, nfa):
    '''
      The key point is to start with epsilon closure of the NFA init state as a new DFA state.
      Then, from that new DFA state, find all reachable states (in NFA graph, including eps transition).
      Those new states will now be a new DFA state (if it's not existed yet), and we repeat the process.
    '''
    eclosure = dict()
    allstates = dict()

    state1 = nfa.get_eps_closure(nfa.init_state)                # We start with the epsilon closure of the nfa.init_state
    eclosure[nfa.init_state] = state1                           # eclosure[s] = epsilon closure of state s

    count = 1                                                   # Counting var to keep track of new states in DFA
    dfa = Automata(nfa.alphabet)
    dfa.set_init_state(count)

    available = [[state1, count]]                               # available[i] = list of [state, idx]                        
    allstates[count] = state1

    count +=1
    while available:
      [src_state, src_idx] = available.pop()                    # Pop a state from available list

      for char in dfa.alphabet:
        # 1. For each symbol in the alphabet, find all the states 
        #    that the src_state can go to (including epsilon transition) 
        #    -> dst_state
        dst_state = nfa.get_transitions(src_state, char)

        for s in list(dst_state)[:]:
          if s not in eclosure:
            eclosure[s] = nfa.get_eps_closure(s)
          dst_state = dst_state.union(eclosure[s])
        
        # 2. Then, check if dst_state is already in the DFA state list
        #    If not, push it to the DFA state list and availabale list
        #    else, get the idx of that dst_state
        if dst_state:
          if dst_state not in allstates.values():
            available.append([dst_state, count])
            allstates[count] = dst_state
            dst_idx = count
            count += 1
          else:
            dst_idx = [k for k, v in allstates.items() if v == dst_state][0]

          # 3. Create a new transition based on src_idx, dst_idx
          dfa.add_transition(src_idx, dst_idx, char)
    
    # 4. In the new list of DFA states, find every states that has 
    #    NFA accept state and mark it DFA accept state
    for val, state in allstates.items():
      if nfa.final_states[0] in state:
          dfa.add_final_states(val)
    
    self.dfa = dfa

class MinimizeDFA():
  def __init__(self, dfa):    
    self.minimizeDFA(dfa)

  def minimizeDFA(self, dfa):
    '''
      The key here is to identify pairs of states that are "distinguishable", in the sense that 
      reading any string from both of them eventually will lead to an accept state in one case, 
      and a non-accept state in the other case. Then we build the definition of distinguishable 
      states recursively.
    '''
    states = list(dfa.states)
    final_states = list(dfa.final_states)
    n = len(states)
    unchecked = dict()
    count = 1
    distinguished = []
    equivalent = dict(zip(range(n), [{s} for s in states]))
    pos = dict(zip(states, range(n)))

    for i in range(n-1):
      for j in range(i+1, n):
        si, sj = states[i], states[j]
        pair_ij, pair_ji = [si, sj], [sj, si]

        if pair_ij in distinguished or pair_ji in distinguished:
          continue
      
        if (si in final_states and sj not in final_states) or (si not in final_states and sj in final_states):
          distinguished.append([si, sj])
          continue

        # 1 - equivalent; 0 - nonequivalent; -1 - unknown
        eq = 1
        to_append = []

        for char in dfa.alphabet:   
          s1, s2 = dfa.get_transitions(si, char), dfa.get_transitions(sj, char)

          assert len(s1) <= 1 and len(s2) <= 1, f'Detected multiple transitions in DFA'
          
          # One is dead state, one is not
          if len(s1) != len(s2):          
            eq = 0
            break

          # Both are dead states
          if len(s1) == 0:                
            continue
        
          # Both are not dead state
          s1, s2 = s1.pop(), s2.pop()     

          if s1 != s2:
            if [s1, s2] in distinguished or [s2, s1] in distinguished:
              eq = 0
              break
            else:
              to_append.append([s1, s2, char])
              eq = -1
        
        if eq == 0:
          distinguished.append(pair_ij)
        elif eq == -1:
          pair_ij.extend(to_append)
          unchecked[count] = pair_ij
          count += 1
        else:
          p1, p2 = pos[states[i]], pos[states[j]]
          if p1 != p2:
            st = equivalent.pop(p2)
            for s in st:
              pos[s] = p1
            equivalent[p1] = equivalent[p1].union(st)

    new_found = True
    while new_found and unchecked:
      new_found = False
      to_remove = set()
      for key, pair in list(unchecked.items()):
        for tr in pair[2:]:
          if [tr[0], tr[1]] in distinguished or [tr[1], tr[0]] in distinguished:
            unchecked.pop(key)
            distinguished.append([pair[0], pair[1]])
            new_found = True
            break
    
    for pair in unchecked.values():
      p1, p2 = pos[pair[0]], pos[pair[1]]

      if p1 != p2:
        st = equivalent.pop(p2)
        for s in st:
          pos[s] = p1
        equivalent[p1] = equivalent[p1].union(st)
    
    if len(equivalent) == len(states):
      self.minDFA = dfa
    else:
      self.minDFA = dfa.rebuild_from_equivalent(pos)

  def match(self, string):
    cur_state = self.minDFA.init_state

    for char in string:
      if char == Automata.epsilon():
        continue
      dst_state = list(self.minDFA.get_transitions(cur_state, char))
      if not dst_state:
        return False
      cur_state = dst_state[0]
    
    if cur_state in self.minDFA.final_states:
      return True

    return False

def main():
  with open('test_regex.txt', 'r') as f1, open('test_string.txt', 'r') as f2:
    regexs = [line.rstrip('\n') for line in f1]
    strings = [line.rstrip('\n') for line in f2]

  with open('test_result.txt', 'w') as f3:
    for regex, string in zip([regexs[69]], [strings[69]]):
      nfa = RegexToNFA(regex)      
      nfa.nfa.display()
      nfa.nfa.drawGraph('graph/NFA')

      dfa = NFAToDFA(nfa.nfa)      
      dfa.dfa.display()
      dfa.dfa.drawGraph('graph/DFA')

      minDFA = MinimizeDFA(dfa.dfa)      
      minDFA.minDFA.display()
      minDFA.minDFA.drawGraph('graph/minDFA')

      print(minDFA.match(string), file=f3)


  with open('test_groundtruth.txt', 'w') as f4:
    import re

    for regex, string in zip(regexs, strings):
      regex = regex.replace('+', '|')
      print(bool(re.match(f'^{regex}$', string)), file=f4)  

  f1.close()
  f2.close()
  f3.close()
  f4.close()

  test()
  
if __name__ == '__main__':
  try:
    main()
  except BaseException as e:
    print("\nFailure:", e)


# class MinimizeDFA:
#   def __init__(self, dfa):    
#     self.minimizeDFA(dfa)

#   def minimizeDFA(self, dfa):
#     states = list(dfa.states)    
#     final_states = dfa.final_states
#     n = len(states)

#     pos = dict(zip(states, range(n)))
#     inv_pos = dict(zip(range(n), states))

#     marked = [[False for _ in range(n)] for _ in range(n)]
#     Q = []

#     # 3. Init marked table
#     for i in range(n-1):
#       for j in range(i+1, n):
#         si, sj = states[i], states[j]

#         if not marked[i][j] and \
#           ((si in final_states and sj not in final_states) or (si not in final_states and sj in final_states)):
#           marked[i][j] = True
#           marked[j][i] = True
#           Q.append([si, sj])
    
#     # 4. Loop to finish marked table
#     while Q:
#       [si, sj] = Q.pop()

#       for char in dfa.alphabet:
#         src_si = dfa.get_inv_transitions(si, char)
#         src_sj = dfa.get_inv_transitions(sj, char)

#         for u, v in itertools.product(src_si, src_sj):
#           pu, pv = pos[u], pos[v]
#           if not marked[pu][pv]:
#             marked[pu][pv] = True
#             marked[pv][pu] = True
#             Q.append([u, v])

#     count = -1
#     checked = [False for _ in range(n)]
#     for i in range(n):
#       if not checked[i]:
#         count += 1
#         pos[states[i]] = count
#         checked[i] = True

#         for j in range(i+1, n):        
#           if not marked[i][j]:        # i, j: same class
#             pos[states[j]] = count
#             checked[j] = True
    
#     self.minDFA = dfa.rebuild_from_equivalent(pos)

#   def match(self, string):
#     cur_state = self.minDFA.init_state

#     for char in string:
#       if char == Automata.epsilon():
#         continue
#       dst_state = list(self.minDFA.get_transitions(cur_state, char))
#       if not dst_state:
#         return False
#       cur_state = dst_state[0]
    
#     if cur_state in self.minDFA.final_states:
#       return True

#     return False
  





