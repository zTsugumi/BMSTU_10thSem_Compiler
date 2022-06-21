int cmp(int *a, int *b)
{
  return *a - *b;
}

int main()
{
  int a = 1;
  int b = 2;

  printf("%d\n", *(&a) + *(&b));
  printf("%d\n", *(&a) - *(&b));
  printf("%d\n", *(&a) * *(&b));
  printf("%d\n", *(&a) / *(&b));
  printf("%d\n", *(&a) % *(&b));
  printf("%d\n", cmp(&a, &b));

  return 0;
}
