#include "codexion.h"

#include <errno.h>
#include <time.h>

static void	lock_pair(t_sim *sim, t_coder *coder)
{
	if (coder->left == coder->right)
		pthread_mutex_lock(&sim->dongles[coder->left].mutex);
	else if (coder->left < coder->right)
	{
		pthread_mutex_lock(&sim->dongles[coder->left].mutex);
		pthread_mutex_lock(&sim->dongles[coder->right].mutex);
	}
	else
	{
		pthread_mutex_lock(&sim->dongles[coder->right].mutex);
		pthread_mutex_lock(&sim->dongles[coder->left].mutex);
	}
}

static void	unlock_pair(t_sim *sim, t_coder *coder)
{
	pthread_mutex_unlock(&sim->dongles[coder->left].mutex);
	if (coder->right != coder->left)
		pthread_mutex_unlock(&sim->dongles[coder->right].mutex);
}

static int	request_is_available(t_sim *sim, int coder_index, long long now)
{
	t_coder	*coder;
	int		available;

	coder = &sim->coders[coder_index];
	if (coder->left == coder->right
		|| now >= coder->last_compile_start + sim->config.burnout_ms)
		return (0);
	lock_pair(sim, coder);
	available = !sim->dongles[coder->left].held
		&& !sim->dongles[coder->right].held
		&& now >= sim->dongles[coder->left].available_at
		&& now >= sim->dongles[coder->right].available_at;
	unlock_pair(sim, coder);
	return (available);
}

static size_t	best_available_request(t_sim *sim, long long now)
{
	size_t	index;
	size_t	best;
	int		is_before;

	index = 0;
	best = sim->heap_size;
	while (index < sim->heap_size)
	{
		if (request_is_available(sim, sim->heap[index].coder_index, now))
		{
			is_before = (best == sim->heap_size);
			if (!is_before && sim->config.scheduler == FIFO)
				is_before = sim->heap[index].order < sim->heap[best].order;
			else if (!is_before)
				is_before = sim->heap[index].deadline
					< sim->heap[best].deadline
					|| (sim->heap[index].deadline == sim->heap[best].deadline
						&& sim->heap[index].order < sim->heap[best].order);
			if (is_before)
				best = index;
		}
		index++;
	}
	return (best);
}

static void	grant_request(t_sim *sim, size_t index, long long now)
{
	t_coder	*coder;

	coder = &sim->coders[sim->heap[index].coder_index];
	heap_remove(sim, index);
	lock_pair(sim, coder);
	sim->dongles[coder->left].held = 1;
	sim->dongles[coder->right].held = 1;
	unlock_pair(sim, coder);
	coder->queued = 0;
	coder->granted = 1;
	coder->last_compile_start = now;
	log_state(sim, coder->id, "has taken a dongle", now - sim->start_ms);
	log_state(sim, coder->id, "has taken a dongle", now - sim->start_ms);
	log_state(sim, coder->id, "is compiling", now - sim->start_ms);
	pthread_cond_broadcast(&sim->condition);
}

void	dispatch_requests(t_sim *sim, long long now)
{
	size_t	best;

	best = best_available_request(sim, now);
	while (best < sim->heap_size && !sim->stop)
	{
		grant_request(sim, best, now);
		now = time_now_ms();
		best = best_available_request(sim, now);
	}
}

static long long	next_cooldown(t_sim *sim, t_coder *coder, long long now)
{
	long long	next;

	next = 0;
	lock_pair(sim, coder);
	if (!sim->dongles[coder->left].held
		&& sim->dongles[coder->left].available_at > now)
		next = sim->dongles[coder->left].available_at;
	if (!sim->dongles[coder->right].held
		&& sim->dongles[coder->right].available_at > now
		&& (next == 0 || sim->dongles[coder->right].available_at < next))
		next = sim->dongles[coder->right].available_at;
	unlock_pair(sim, coder);
	return (next);
}

static void	make_deadline(struct timespec *deadline, long long time_ms)
{
	deadline->tv_sec = (time_t)(time_ms / 1000);
	deadline->tv_nsec = (long)(time_ms % 1000) * 1000000L;
}

static void	remove_coder_request(t_sim *sim, int coder_index)
{
	size_t	index;

	index = 0;
	while (index < sim->heap_size)
	{
		if (sim->heap[index].coder_index == coder_index)
		{
			heap_remove(sim, index);
			break ;
		}
		index++;
	}
}

int	request_dongles(t_coder *coder)
{
	t_sim			*sim;
	long long		now;
	long long		cooldown_at;
	struct timespec	deadline;
	int				result;

	sim = coder->sim;
	pthread_mutex_lock(&sim->mutex);
	if (sim->stop || !heap_push(sim, coder->id - 1))
	{
		pthread_mutex_unlock(&sim->mutex);
		return (0);
	}
	coder->queued = 1;
	dispatch_requests(sim, time_now_ms());
	while (!sim->stop && !coder->granted)
	{
		now = time_now_ms();
		cooldown_at = next_cooldown(sim, coder, now);
		if (cooldown_at > 0)
		{
			make_deadline(&deadline, cooldown_at);
			result = pthread_cond_timedwait(&sim->condition, &sim->mutex,
					&deadline);
		}
		else
			result = pthread_cond_wait(&sim->condition, &sim->mutex);
		if (result != 0 && result != ETIMEDOUT)
		{
			sim->stop = 1;
			pthread_cond_broadcast(&sim->condition);
		}
		dispatch_requests(sim, time_now_ms());
	}
	if (coder->queued)
	{
		remove_coder_request(sim, coder->id - 1);
		coder->queued = 0;
	}
	result = coder->granted;
	pthread_mutex_unlock(&sim->mutex);
	return (result);
}
