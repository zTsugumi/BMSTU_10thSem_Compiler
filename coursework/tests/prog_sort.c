int a[8] = {5, 4, 3, 3, 4, 5, 1, 2};

int main()
{
  int i, j, n, temp;

  i = 0;
  n = 8;
  printf("Before sort: ");
  while (i < n)
  {
    printf("%d ", a[i]);
    i = i + 1;
  }

  i = 0;
  while (i < n - 1)
  {
    j = i + 1;
    while (j < n)
    {
      if (a[i] > a[j])
      {
        temp = a[i];
        a[i] = a[j];
        a[j] = temp;
      }
      j = j + 1;
    }
    i = i + 1;
  }

  i = 0;
  printf("\nAfter sort: ");
  while (i < n)
  {
    printf("%d ", a[i]);
    i = i + 1;
  }

  return 0;
}
