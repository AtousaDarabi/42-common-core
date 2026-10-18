#include "codexion.h"

void	print_state(t_coder *c, const char *msg)
{
	t_data	*d;

	d = c->data;
	pthread_mutex_lock(&d->log_mutex);
	if (!is_stopped(d))
		printf("%ld %d %s\n", elapsed_ms(d), c->id, msg);
	pthread_mutex_unlock(&d->log_mutex);
}

void	print_burnout(t_data *d, int id)
{
	pthread_mutex_lock(&d->log_mutex);
	if (!is_stopped(d))
	{
		set_stop(d);
		printf("%ld %d burned out\n", elapsed_ms(d), id);
	}
	pthread_mutex_unlock(&d->log_mutex);
}
