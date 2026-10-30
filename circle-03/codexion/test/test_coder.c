#include "../codexion.h"

/* parse.c needs this; main.c is not linked into the test. */
int	error_msg(const char *msg)
{
	fprintf(stderr, "Error: %s\n", msg);
	return (1);
}

static void	report(t_data *d)
{
	int	i;

	i = 0;
	fprintf(stderr, "  compiles per coder:");
	while (i < d->cfg.n && i < 12)
	{
		fprintf(stderr, " %d", d->coders[i].compiles);
		i++;
	}
	fprintf(stderr, "%s\n", d->cfg.n > 12 ? " ..." : "");
}

/* usage: test_coder.out <the 8 normal args> <run_ms> */
int	main(int ac, char **av)
{
	t_data	d;

	memset(&d, 0, sizeof(d));
	if (ac != 10 || parse_args(ac - 1, av, &d.cfg))
		return (1);
	if (sim_init(&d))
		return (1);
	if (start_threads(&d))
	{
		sim_destroy(&d);
		return (1);
	}
	usleep(atol(av[9]) * 1000);
	set_stop(&d);
	dongle_wake_all(&d);
	join_threads(&d, d.cfg.n);
	report(&d);
	sim_destroy(&d);
	return (0);
}
