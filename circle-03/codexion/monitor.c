#include "codexion.h"

/* 1 when every coder has finished at least n_compiles compiles. */
static int	all_done(t_data *d)
{
	t_coder	*c;
	int		i;
	int		done;

	i = 0;
	while (i < d->cfg.n)
	{
		c = &d->coders[i];
		pthread_mutex_lock(&c->lock);
		done = (c->compiles >= d->cfg.n_compiles);
		pthread_mutex_unlock(&c->lock);
		if (!done)
			return (0);
		i++;
	}
	return (1);
}

/* 1 if a coder burned out (message printed, simulation stopped). */
static int	check_burnout(t_data *d)
{
	t_coder	*c;
	long	last;
	int		i;

	i = 0;
	while (i < d->cfg.n)
	{
		c = &d->coders[i];
		pthread_mutex_lock(&c->lock);
		last = c->last_compile_start;
		pthread_mutex_unlock(&c->lock);
		if (get_time_ms() - last >= d->cfg.t_burnout)
		{
			print_burnout(d, c->id);
			dongle_wake_all(d);
			return (1);
		}
		i++;
	}
	return (0);
}

void	*monitor_routine(void *arg)
{
	t_data	*d;

	d = arg;
	while (!is_stopped(d))
	{
		if (all_done(d))
		{
			set_stop(d);
			dongle_wake_all(d);
			break ;
		}
		if (check_burnout(d))
			break ;
		usleep(1000);
	}
	return (NULL);
}
