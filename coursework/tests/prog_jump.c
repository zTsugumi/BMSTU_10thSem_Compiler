int main()
{
  int i = 0;
  while (i < 10)
  {
    if (i % 2)
    {
      i = i + 1;
      continue;
    }
    else
      printf("%d", i);
    if (i == 7)
      break;
    i = i + 1;
  }

  return 0;
}