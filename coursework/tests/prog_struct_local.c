int main()
{
	struct S
	{
		int mem;
	};

	struct R
	{
		int mem;
	} my_r1, *my_r2;

	struct S a;
	struct S *b;

	a.mem = 1;
	b->mem = 2;
	my_r1.mem = 3;
	my_r2->mem = 4;

	printf("%d", a.mem);
	printf("%d", b->mem);
	printf("%d", my_r1.mem);
	printf("%d", my_r2->mem);
	return 0;
}