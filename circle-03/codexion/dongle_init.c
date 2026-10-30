#include "codexion.h"

static int	init_one(t_dongle *dg)
{
	if (heap_init(&dg->queue, 2))
		return (1);
	if (pthread_mutex_init(&dg->mutex, NULL))
	{
		heap_free(&dg->queue);
		return (1);
	}
	if (pthread_cond_init(&dg->cond, NULL))
	{
		pthread_mutex_destroy(&dg->mutex);
		heap_free(&dg->queue);
		return (1);
	}
	dg->in_use = 0;
	dg->free_at = 0;
	return (0);
}

int	dongle_init(t_data *d)
{
	int	i;

	d->dongles = malloc(sizeof(t_dongle) * d->cfg.n);
	if (!d->dongles)
		return (1);
	memset(d->dongles, 0, sizeof(t_dongle) * d->cfg.n);
	i = 0;
	while (i < d->cfg.n)
	{
		if (init_one(&d->dongles[i]))
		{
			dongle_destroy(d, i);
			return (1);
		}
		i++;
	}
	return (0);
}

void	dongle_destroy(t_data *d, int count)
{
	int	i;

	i = 0;
	while (i < count)
	{
		pthread_mutex_destroy(&d->dongles[i].mutex);
		pthread_cond_destroy(&d->dongles[i].cond);
		heap_free(&d->dongles[i].queue);
		i++;
	}
	free(d->dongles);
	d->dongles = NULL;
}
