#include "../codexion.h"
#include <unistd.h>

static void	*spam(void *arg)
{
	t_coder	*c;
	int		i;

	c = arg;
	i = 0;
	while (i < 2000)
	{
		print_state(c, "is compiling");
		i++;
	}
	return (NULL);
}

static void	test_time(t_data *d)
{
	long	before;

	before = elapsed_ms(d);
	usleep(100000);
	printf("elapsed after 100ms sleep (expect ~100): %ld\n",
		elapsed_ms(d) - before);
}

int	main(void)
{
	t_data		d;
	t_coder		c[4];
	pthread_t	t[4];
	int			i;

	memset(&d, 0, sizeof(d));
	pthread_mutex_init(&d.log_mutex, NULL);
	pthread_mutex_init(&d.stop_mutex, NULL);
	d.start_ms = get_time_ms();
	test_time(&d);
	i = -1;
	while (++i < 4)
	{
		c[i].id = i + 1;
		c[i].data = &d;
		pthread_create(&t[i], NULL, spam, &c[i]);
	}
	print_burnout(&d, 99);
	i = -1;
	while (++i < 4)
		pthread_join(t[i], NULL);
	print_state(&c[0], "SHOULD NOT APPEAR");
	return (0);
}
