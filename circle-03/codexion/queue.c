#include "codexion.h"

static int	request_before(t_sim *sim, const t_request *first,
		const t_request *second)
{
	if (sim->config.scheduler == EDF && first->deadline != second->deadline)
		return (first->deadline < second->deadline);
	return (first->order < second->order);
}

static void	swap_requests(t_request *first, t_request *second)
{
	t_request	temp;

	temp = *first;
	*first = *second;
	*second = temp;
}

static void	heap_up(t_sim *sim, size_t index)
{
	size_t	parent;

	while (index > 0)
	{
		parent = (index - 1) / 2;
		if (!request_before(sim, &sim->heap[index], &sim->heap[parent]))
			break ;
		swap_requests(&sim->heap[index], &sim->heap[parent]);
		index = parent;
	}
}

static void	heap_down(t_sim *sim, size_t index)
{
	size_t	left;
	size_t	right;
	size_t	best;

	while (index * 2 + 1 < sim->heap_size)
	{
		left = index * 2 + 1;
		right = left + 1;
		best = left;
		if (right < sim->heap_size
			&& request_before(sim, &sim->heap[right], &sim->heap[left]))
			best = right;
		if (!request_before(sim, &sim->heap[best], &sim->heap[index]))
			break ;
		swap_requests(&sim->heap[index], &sim->heap[best]);
		index = best;
	}
}

int	heap_push(t_sim *sim, int coder_index)
{
	t_request	*request;

	if (sim->heap_size >= (size_t)sim->config.coder_count)
		return (0);
	request = &sim->heap[sim->heap_size];
	request->coder_index = coder_index;
	request->order = sim->next_order++;
	request->deadline = sim->coders[coder_index].last_compile_start
		+ sim->config.burnout_ms;
	sim->heap_size++;
	heap_up(sim, sim->heap_size - 1);
	return (1);
}

int	heap_remove(t_sim *sim, size_t index)
{
	size_t	parent;

	if (index >= sim->heap_size)
		return (0);
	sim->heap_size--;
	if (index < sim->heap_size)
	{
		sim->heap[index] = sim->heap[sim->heap_size];
		if (index > 0)
		{
			parent = (index - 1) / 2;
			if (request_before(sim, &sim->heap[index], &sim->heap[parent]))
			{
				heap_up(sim, index);
				return (1);
			}
		}
		heap_down(sim, index);
	}
	return (1);
}
