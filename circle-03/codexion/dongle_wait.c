#include "codexion.h"

static int	is_my_turn(t_dongle *dg, int id)
{
	t_req	top;

	if (heap_peek(&dg->queue, &top))
		return (0);
	return (top.coder_id == id);
}

static void	wait_cooldown(t_dongle *dg)
{
	struct timespec	ts;

	ts.tv_sec = dg->free_at / 1000;
	ts.tv_nsec = (dg->free_at % 1000) * 1000000L;
	pthread_cond_timedwait(&dg->cond, &dg->mutex, &ts);
}

/* Called with dg->mutex locked. Returns 0 = dongle is ours, 1 = stopped. */
int	dongle_wait(t_coder *c, t_dongle *dg)
{
	int	my_turn;

	while (!is_stopped(c->data))
	{
		my_turn = is_my_turn(dg, c->id);
		if (my_turn && !dg->in_use && get_time_ms() >= dg->free_at)
			return (0);
		if (my_turn && !dg->in_use)
			wait_cooldown(dg);
		else
			pthread_cond_wait(&dg->cond, &dg->mutex);
	}
	return (1);
}
