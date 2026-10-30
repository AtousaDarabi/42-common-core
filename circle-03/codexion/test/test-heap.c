#include "../codexion.h"

static void	check(const char *name, int ok)
{
	printf("%-28s %s\n", name, ok ? "PASS" : "FAIL");
}

static void	test_order(void)
{
	t_heap	h;
	t_req	r;
	long	prev;
	int		i;
	int		ok;

	heap_init(&h, 100);
	i = 0;
	while (i < 100)
	{
		heap_push(&h, i, (i * 37) % 23 + 5);
		i++;
	}
	prev = -1;
	ok = 1;
	while (!heap_pop(&h, &r))
	{
		if (r.key < prev)
			ok = 0;
		prev = r.key;
	}
	check("sorted by key", ok);
	heap_free(&h);
}

static void	test_fifo_and_edf(void)
{
	t_heap	h;
	t_req	a;
	t_req	b;
	t_req	c;

	heap_init(&h, 4);
	heap_push(&h, 7, 0);
	heap_push(&h, 3, 0);
	heap_push(&h, 9, 0);
	heap_pop(&h, &a);
	heap_pop(&h, &b);
	heap_pop(&h, &c);
	check("fifo (key 0): 7,3,9", a.coder_id == 7 && b.coder_id == 3
		&& c.coder_id == 9);
	heap_push(&h, 1, 900);
	heap_push(&h, 2, 800);
	heap_push(&h, 3, 850);
	heap_pop(&h, &a);
	heap_pop(&h, &b);
	heap_pop(&h, &c);
	check("edf (deadline): 2,3,1", a.coder_id == 2 && b.coder_id == 3
		&& c.coder_id == 1);
	heap_free(&h);
}

static void	test_limits(void)
{
	t_heap	h;
	t_req	r;

	heap_init(&h, 2);
	check("pop on empty fails", heap_pop(&h, &r) == 1);
	check("peek on empty fails", heap_peek(&h, &r) == 1);
	heap_push(&h, 1, 5);
	heap_push(&h, 2, 3);
	check("push on full fails", heap_push(&h, 3, 1) == 1);
	heap_peek(&h, &r);
	check("peek = smallest, no remove", r.coder_id == 2 && h.size == 2);
	heap_free(&h);
}

int	main(void)
{
	test_order();
	test_fifo_and_edf();
	test_limits();
	return (0);
}
