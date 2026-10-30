#include "codexion.h"

static void	set_start_times(t_data *d)
{
	int	i;

	d->start_ms = get_time_ms();
	i = 0;
	while (i < d->cfg.n)
	{
		d->coders[i].last_compile_start = d->start_ms;
		i++;
	}
}

void	join_threads(t_data *d, int count)
{
	int	i;

	i = 0;
	while (i < count)
	{
		pthread_join(d->coders[i].thread, NULL);
		i++;
	}
}

int	start_threads(t_data *d)
{
	int	i;

	set_start_times(d);
	i = 0;
	while (i < d->cfg.n)
	{
		if (pthread_create(&d->coders[i].thread, NULL, coder_routine,
				&d->coders[i]))
		{
			set_stop(d);
			dongle_wake_all(d);
			join_threads(d, i);
			return (1);
		}
		i++;
	}
	return (0);
}

int	run_simulation(t_data *d)
{
	pthread_t	monitor;

	if (start_threads(d))
		return (1);
	if (pthread_create(&monitor, NULL, monitor_routine, d))
	{
		set_stop(d);
		dongle_wake_all(d);
		join_threads(d, d->cfg.n);
		return (1);
	}
	pthread_join(monitor, NULL);
	join_threads(d, d->cfg.n);
	return (0);
}
