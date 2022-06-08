from cfg import CFG, eliminate_left_recursion, left_factor, remove_useless

def main():
  fi = './test/res2.elr.txt'
  fo = './test/res3.elr.txt'

  # cfg = CFG(fi)
  # cfg_elr = eliminate_left_recursion(cfg)
  # cfg_elr.export_to_file(fo)

  # cfg = CFG(fi)
  # cfg_factor = left_factor(cfg)
  # cfg_factor.export_to_file(fo)

  cfg = CFG(fi)
  cfg_no_useless = remove_useless(cfg)
  cfg_no_useless.export_to_file(fo)


if __name__ == '__main__':
  try:
    main()
  except BaseException as e:
    print("\nFailure:", e)