
#include "../codexion.h"

static void	*grab(void *arg)
{
	t_coder	*c;

	c = arg;
	if (dongle_acquire(c, &c->data->dongles[0]))
	{
		printf("  coder %d: stopped while waiting\n", c->id);
		return (NULL);
	}
	printf("  coder %d got dongle at %ld ms\n", c->id, elapsed_ms(c->data));
	usleep(20000);
	dongle_release(c, &c->data->dongles[0]);
	return (NULL);
}

static void	setup(t_data *d, t_coder *c, t_sched s)
{
	int	i;

	memset(d, 0, sizeof(*d));
	d->cfg.n = 1;
	d->cfg.sched = s;
	d->cfg.t_burnout = 1000;
	d->cfg.cooldown = 50;
	pthread_mutex_init(&d->log_mutex, NULL);
	pthread_mutex_init(&d->stop_mutex, NULL);
	dongle_init(d);
	heap_free(&d->dongles[0].queue);
	heap_init(&d->dongles[0].queue, 4);
	d->start_ms = get_time_ms();
	i = 0;
	while (i < 4)
	{
		c[i].id = i;
		c[i].data = d;
		pthread_mutex_init(&c[i].lock, NULL);
		c[i].last_compile_start = d->start_ms;
		i++;
	}
}

static void	run(t_sched s, long *offs)
{
	t_data		d;
	t_coder		c[4];
	pthread_t	t[4];
	int			i;

	setup(&d, c, s);
	i = 0;
	while (i++ < 3)
		c[i].last_compile_start += offs[i - 1];
	dongle_acquire(&c[0], &d.dongles[0]);
	i = 0;
	while (i++ < 3)
	{
		pthread_create(&t[i], NULL, grab, &c[i]);
		usleep(10000);
	}
	dongle_release(&c[0], &d.dongles[0]);
	i = 0;
	while (i++ < 3)
		pthread_join(t[i], NULL);
	dongle_destroy(&d, 1);
}

static void	run_stop(void)
{
	t_data		d;
	t_coder		c[4];
	pthread_t	t;

	setup(&d, c, SCHEDULER_FIFO);
	dongle_acquire(&c[0], &d.dongles[0]);
	pthread_create(&t, NULL, grab, &c[1]);
	usleep(50000);
	set_stop(&d);
	dongle_wake_all(&d);
	pthread_join(t, NULL);
	dongle_destroy(&d, 1);
}

int	main(void)
{
	long	edf[3];

	edf[0] = 300;
	edf[1] = 100;
	edf[2] = 200;
	printf("FIFO (expect 1,2,3 ~70 ms apart):\n");
	run(SCHEDULER_FIFO, edf);
	printf("EDF (expect 2,3,1 ~70 ms apart):\n");
	run(SCHEDULER_EDF, edf);
	printf("STOP (expect coder 1 stopped, no hang):\n");
	run_stop();
	return (0);
}
