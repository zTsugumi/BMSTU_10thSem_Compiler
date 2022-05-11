def test():
  with open('test_result.txt', 'r') as f1, open('test_groundtruth.txt', 'r') as f2:
    results = [line.rstrip('\n') for line in f1]
    groundtruth = [line.rstrip('\n') for line in f2]

  ok = True
  for res, gt in zip(results, groundtruth):
    if res != gt:
      print('WA')
      ok = False
      break
  
  if ok:
    print('AC')