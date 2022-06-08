from itertools import takewhile


class CFG:
  def __init__(self, cfg_file=None):
    if cfg_file is not None:
      self.build_cfg(cfg_file)
    else:
      self.terminal = set()
      self.nonterminal = set()
      self.production = dict()
      self.s = str()

  def build_cfg(self, cfg_file):
    with open(cfg_file, 'r') as f:
      lines = f.readlines()

    n_nonterminal = int(lines[0])
    self.nonterminal = set(lines[1].rstrip('\n').split(' '))
    assert len(self.nonterminal) == n_nonterminal

    n_terminal = int(lines[2])
    self.terminal = set(lines[3].rstrip('\n').split(' '))
    assert len(self.terminal) == n_terminal

    n_production = int(lines[4])
    self.production = dict()
    for i in range(n_production):
      rule = lines[i + 5].rstrip('\n').replace(' ', '').split('->')
      options = rule[1].split('|')

      if rule[0] in self.production:
        self.production[rule[0]] = self.production[rule[0]].union(options)
      else:
        self.production[rule[0]] = set(options)

    self.s = lines[-1].rstrip('\n')[0]

  def update_production(self, Ai, Ai_rule, new_rules):
    self.production[Ai].discard(Ai_rule)
    self.production[Ai] = self.production[Ai].union(new_rules)

  def export_to_file(self, file):
    with open(file, 'w', encoding='utf-8') as f:
      f.write(f'{len(self.nonterminal)}\n')
      f.write(' '.join(self.nonterminal) + '\n')
      f.write(f'{len(self.terminal)}\n')
      f.write(' '.join(self.terminal) + '\n')
      f.write(f'{len(self.production)}\n')
      for (key, vals) in self.production.items():
        f.write(f'{key} -> {" | ".join(vals)}\n')
      f.write(self.s)


def eliminate_left_recursion(cfg_src):
  '''
  Algo 4.19 - Compilers - Principles, Techniques, and Tools / P.238
  '''
  cfg = cfg_src

  g = CFG()
  g.terminal = cfg.terminal
  g.nonterminal = cfg.nonterminal
  g.s = cfg.s

  A = list(cfg.nonterminal)
  for i in range(len(A)):
    Ai = A[i]
    Ai_rules = cfg.production[Ai]

    # 1. Replace each production of the form Ai -> AjY
    #    by the productions:
    #          Ai -> B0Y | B1Y | ... | BkY
    #    where,
    #          Aj -> B0 | B1 | ... | Bk
    #    are all the current Aj-productions
    for j in range(i):
      Aj = A[j]
      Aj_rules = cfg.production[Aj]

      for Ai_rule in Ai_rules.copy():
        if Ai_rule.startswith(Aj):
          remain_i = Ai_rule[len(Aj):]

          new_rules = set([Aj_rule + remain_i
                              for Aj_rule in Aj_rules])

          cfg.update_production(Ai, Ai_rule, new_rules)

    # 2. Eliminate the immediate left recursion among Ai-productions
    Ai = A[i]
    Ai_rules = cfg.production[A[i]]

    if any(rule.startswith(Ai) for rule in Ai_rules):  # Left-recursion
      alpha = set([rule for rule in Ai_rules if rule.startswith(Ai)])
      beta = Ai_rules.difference(alpha)

      new_symbol = Ai + "'"

      if beta:
        beta_rules = set([c + new_symbol for c in beta])
      else:
        beta_rules = set([new_symbol])

      alpha_rules = set([c[len(Ai):] + new_symbol for c in alpha])
      alpha_rules.add('ε')

      g.nonterminal.add(new_symbol)
      g.production.update({Ai: beta_rules})
      g.production.update({new_symbol: alpha_rules})
      cfg.production[Ai] = beta_rules
    else:
      g.production.update({Ai: Ai_rules})

  return g


def left_factor(cfg_src):
  '''
  Algo 4.21 - Compilers - Principles, Techniques, and Tools / P.240
  '''
  cfg = cfg_src
  g = CFG()
  g.terminal = cfg.terminal
  g.nonterminal = cfg.nonterminal
  g.s = cfg.s

  found_alpha = True
  while found_alpha:
    A = list(cfg.nonterminal)
    found_alpha = False

    for i in range(len(A)):
      Ai = A[i]
      Ai_rules = cfg.production[Ai]
      new_symbol = Ai + "'"

      alpha = find_common(Ai_rules)

      if alpha:
        found_alpha = True
        alpha_rules = set([alpha + new_symbol] +
                          [rule for rule in Ai_rules if not rule.startswith(alpha)])
        beta_rules = set([rule[len(alpha):] for rule in Ai_rules if rule.startswith(alpha)])
        beta_rules = set(['ε' if not rule else rule for rule in beta_rules])

        g.nonterminal.add(new_symbol)
        g.production.update({Ai: alpha_rules})
        g.production.update({new_symbol: beta_rules})
      else:
        g.production.update({Ai: Ai_rules})

    cfg = g

  return g


def find_common(lst):
  lst = list(lst)

  res = ''
  max_size = 0
  for i, s1 in enumerate(lst):
    for s2 in lst[i + 1:]:
      common = ''.join(c[0] for c in takewhile(lambda x: all(x[0] == y for y in x), zip(*[s1, s2])))
      max_size = max(max_size, len(common))
      if max_size == len(common):
        res = common

  return res


def remove_useless(cfg_src):
  '''
  Algo 2.7 + 2.8 + 2.9 - The theory of Parsing, Translation, and Compiling / Page 163
  '''
  def get_Ne(cfg):
    '''
    Algo 2.7 - The theory of Parsing, Translation, and Compiling / Page 163
    '''
    Ne = set()

    while True:
      alpha_set = Ne.union(cfg.terminal, 'ε')

      Ni = set()
      for (key, vals) in cfg.production.items():
        if any(val in alpha_set for val in vals):
          Ni = Ni.union(key)

      Ni = Ni.union(Ne)

      if Ni == Ne:
        break

      Ne = Ni

    return Ne

  def remove_inaccessible(cfg):
    '''
    Algo 2.8 - The theory of Parsing, Translation, and Compiling / Page 163
    '''
    V0 = set(cfg.s)

    while True:
      Vi = set()

      for X in cfg.nonterminal.union(cfg.terminal):
        for A in V0:
          if A not in cfg.production.keys(): continue
          if any(X in val for val in cfg.production[A]):
            Vi = Vi.union(X)
            break

      Vi = Vi.union(V0)

      if Vi == V0:
        break

      V0 = Vi

    return Vi

  cfg = cfg_src
  Ne = get_Ne(cfg)

  if cfg.s in Ne:     # cfg not empty
    # Step 1 in Algo 2.9 ~ Algo 2.7
    g1 = CFG()
    g1.nonterminal = cfg.nonterminal.intersection(Ne)
    g1.terminal = cfg.terminal
    g1.s = cfg.s

    NeSigma = Ne.union(g1.terminal)
    for (key, vals) in cfg.production.items():
      if key not in NeSigma: continue
      newvals = set([val for val in vals if val in NeSigma])
      g1.production.update({key: newvals})

    # Step 2 in Algo 2.9 ~ Algo 2.8
    Vi = remove_inaccessible(g1)
    g2 = CFG()
    g2.nonterminal = g1.nonterminal.intersection(Vi)
    g2.terminal = g1.terminal.intersection(Vi)
    for (key, vals) in cfg.production.items():
      if key not in Vi: continue
      newvals = set([val for val in vals if val in Vi])
      g2.production.update({key: newvals})
    g2.s = g1.s
  else:
    raise Exception('Empty grammar!')

  return g2


