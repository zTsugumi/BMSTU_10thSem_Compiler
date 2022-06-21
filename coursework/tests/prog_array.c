int a[5] = {1, 2, 3, 4, 5};

int main()
{
  int b[5] = {5, 4, 3, 2, 1};

  int i = 0;
  while (i <= 4)
  {
    int c = a[i] - b[i];
    printf("%d ", c);
    i = i + 1;
  }

  return 0;
}