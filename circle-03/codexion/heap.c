#include "codexion.h"

int	heap_init(t_heap *h, int cap)
{
	h->arr = malloc(sizeof(t_req) * cap);
	if (!h->arr)
		return (1);
	h->size = 0;
	h->cap = cap;
	h->next_seq = 0;
	return (0);
}

void	heap_free(t_heap *h)
{
	free(h->arr);
	h->arr = NULL;
	h->size = 0;
}

int	heap_push(t_heap *h, int coder_id, long key)
{
	if (h->size >= h->cap)
		return (1);
	h->arr[h->size].coder_id = coder_id;
	h->arr[h->size].key = key;
	h->arr[h->size].seq = h->next_seq++;
	h->size++;
	sift_up(h, h->size - 1);
	return (0);
}

int	heap_peek(t_heap *h, t_req *out)
{
	if (h->size == 0)
		return (1);
	*out = h->arr[0];
	return (0);
}

int	heap_pop(t_heap *h, t_req *out)
{
	if (h->size == 0)
		return (1);
	*out = h->arr[0];
	h->size--;
	h->arr[0] = h->arr[h->size];
	sift_down(h, 0);
	return (0);
}
