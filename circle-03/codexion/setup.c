#include "codexion.h"

static void	destroy_mutexes(t_data *d)
{
	pthread_mutex_destroy(&d->log_mutex);
	pthread_mutex_destroy(&d->stop_mutex);
}

int	sim_init(t_data *d)
{
	if (pthread_mutex_init(&d->log_mutex, NULL))
		return (1);
	if (pthread_mutex_init(&d->stop_mutex, NULL))
	{
		pthread_mutex_destroy(&d->log_mutex);
		return (1);
	}
	if (dongle_init(d))
	{
		destroy_mutexes(d);
		return (1);
	}
	if (init_coders(d))
	{
		dongle_destroy(d, d->cfg.n);
		destroy_mutexes(d);
		return (1);
	}
	return (0);
}

void	sim_destroy(t_data *d)
{
	destroy_coders(d, d->cfg.n);
	dongle_destroy(d, d->cfg.n);
	destroy_mutexes(d);
}
