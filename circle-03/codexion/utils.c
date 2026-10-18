#include "codexion.h"

long	get_time_ms(void)
{
	struct timeval	tv;

	gettimeofday(&tv, NULL);
	return (tv.tv_sec * 1000L + tv.tv_usec / 1000);
}

long	elapsed_ms(t_data *d)
{
	return (get_time_ms() - d->start_ms);
}

int	is_stopped(t_data *d)
{
	int	res;

	pthread_mutex_lock(&d->stop_mutex);
	res = d->stop;
	pthread_mutex_unlock(&d->stop_mutex);
	return (res);
}

void	set_stop(t_data *d)
{
	pthread_mutex_lock(&d->stop_mutex);
	d->stop = 1;
	pthread_mutex_unlock(&d->stop_mutex);
}
