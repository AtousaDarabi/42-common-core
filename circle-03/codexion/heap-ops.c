#include "codexion.h"

int	req_less(t_req *a, t_req *b)
{
	if (a->key != b->key)
		return (a->key < b->key);
	return (a->seq < b->seq);
}

static void	swap_req(t_req *a, t_req *b)
{
	t_req	tmp;

	tmp = *a;
	*a = *b;
	*b = tmp;
}

void	sift_up(t_heap *h, int i)
{
	int	parent;

	while (i > 0)
	{
		parent = (i - 1) / 2;
		if (!req_less(&h->arr[i], &h->arr[parent]))
			break ;
		swap_req(&h->arr[i], &h->arr[parent]);
		i = parent;
	}
}

void	sift_down(t_heap *h, int i)
{
	int	small;
	int	l;
	int	r;

	while (1)
	{
		l = 2 * i + 1;
		r = l + 1;
		small = i;
		if (l < h->size && req_less(&h->arr[l], &h->arr[small]))
			small = l;
		if (r < h->size && req_less(&h->arr[r], &h->arr[small]))
			small = r;
		if (small == i)
			return ;
		swap_req(&h->arr[i], &h->arr[small]);
		i = small;
	}
}
