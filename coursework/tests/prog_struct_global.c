struct S
{
	int mem;
};

int main()
{
	struct S a;
	struct S *b;
	a.mem = 1;
	b->mem = 2;

	printf("%d", a.mem);
	printf("%d", b->mem);
	return 0;
}