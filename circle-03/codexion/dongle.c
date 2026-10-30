#include "codexion.h"

static long	get_key(t_coder *c)
{
	long	key;

	if (c->data->cfg.sched == SCHEDULER_FIFO)
		return (0);
	pthread_mutex_lock(&c->lock);
	key = c->last_compile_start + c->data->cfg.t_burnout;
	pthread_mutex_unlock(&c->lock);
	return (key);
}

/* Returns 0 when the dongle is taken, 1 when the simulation stopped. */
int	dongle_acquire(t_coder *c, t_dongle *dg)
{
	t_req	req;
	long	key;
	int		stopped;

	key = get_key(c);
	pthread_mutex_lock(&dg->mutex);
	if (heap_push(&dg->queue, c->id, key))
	{
		pthread_mutex_unlock(&dg->mutex);
		return (1);
	}
	stopped = dongle_wait(c, dg);
	if (!stopped)
	{
		heap_pop(&dg->queue, &req);
		dg->in_use = 1;
	}
	pthread_mutex_unlock(&dg->mutex);
	return (stopped);
}

void	dongle_release(t_coder *c, t_dongle *dg)
{
	pthread_mutex_lock(&dg->mutex);
	dg->in_use = 0;
	dg->free_at = get_time_ms() + c->data->cfg.cooldown;
	pthread_cond_broadcast(&dg->cond);
	pthread_mutex_unlock(&dg->mutex);
}

/* Call AFTER set_stop(): wakes every coder blocked on a dongle. */
void	dongle_wake_all(t_data *d)
{
	int	i;

	i = 0;
	while (i < d->cfg.n)
	{
		pthread_mutex_lock(&d->dongles[i].mutex);
		pthread_cond_broadcast(&d->dongles[i].cond);
		pthread_mutex_unlock(&d->dongles[i].mutex);
		i++;
	}
}
