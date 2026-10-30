#include "codexion.h"

int	error_msg(const char *msg)
{
	fprintf(stderr, "Error: %s\n", msg);
	return (1);
}

int	main(int ac, char **av)
{
	t_data	d;

	memset(&d, 0, sizeof(d));
	if (parse_args(ac, av, &d.cfg))
		return (1);
	if (sim_init(&d))
		return (error_msg("initialization failed"));
	if (run_simulation(&d))
	{
		sim_destroy(&d);
		return (error_msg("could not start the simulation"));
	}
	sim_destroy(&d);
	return (0);
}
