#include "codexion.h"

static void	do_compile(t_coder *c)
{
	t_data	*d;

	d = c->data;
	pthread_mutex_lock(&c->lock);
	c->last_compile_start = get_time_ms();
	pthread_mutex_unlock(&c->lock);
	print_state(c, "is compiling");
	sleep_ms(d, d->cfg.t_compile);
	pthread_mutex_lock(&c->lock);
	c->compiles++;
	pthread_mutex_unlock(&c->lock);
	release_dongles(c);
}

void	*coder_routine(void *arg)
{
	t_coder	*c;
	t_data	*d;

	c = arg;
	d = c->data;
	while (!is_stopped(d))
	{
		if (take_dongles(c))
			break ;
		do_compile(c);
		print_state(c, "is debugging");
		sleep_ms(d, d->cfg.t_debug);
		print_state(c, "is refactoring");
		sleep_ms(d, d->cfg.t_refactor);
	}
	return (NULL);
}
