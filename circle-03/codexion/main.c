#include "codexion.h"

#include <stdlib.h>
#include <unistd.h>

static int	start_threads(t_sim *sim, pthread_t *threads,
		pthread_t *monitor, int *created, int *monitor_created)
{
	int	index;

	if (pthread_create(monitor, NULL, run_monitor, sim) != 0)
		return (0);
	*monitor_created = 1;
	index = 0;
	while (index < sim->config.coder_count)
	{
		if (pthread_create(&threads[index], NULL, run_coder,
				&sim->coders[index]) != 0)
		{
			*created = index;
			stop_simulation(sim);
			return (0);
		}
		index++;
	}
	*created = index;
	return (1);
}

int	main(int argc, char **argv)
{
	t_config	config;
	t_sim		sim;
	pthread_t	*threads;
	pthread_t	monitor;
	int			created;
	int			monitor_created;
	int			result;
	int			index;

	if (!parse_arguments(argc, argv, &config))
	{
		write(STDERR_FILENO, "Usage: ./codexion coders burnout_ms compile_ms "
			"debug_ms refactor_ms required_compiles cooldown_ms fifo|edf\n",
			sizeof("Usage: ./codexion coders burnout_ms compile_ms "
				"debug_ms refactor_ms required_compiles cooldown_ms fifo|edf\n")
			- 1);
		return (1);
	}
	if (!sim_init(&sim, &config))
	{
		sim_destroy(&sim);
		write(STDERR_FILENO, "codexion: initialization failed\n",
			sizeof("codexion: initialization failed\n") - 1);
		return (1);
	}
	threads = malloc((size_t)config.coder_count * sizeof(*threads));
	if (threads == NULL)
	{
		sim_destroy(&sim);
		write(STDERR_FILENO, "codexion: thread allocation failed\n",
			sizeof("codexion: thread allocation failed\n") - 1);
		return (1);
	}
	created = 0;
	monitor_created = 0;
	result = start_threads(&sim, threads, &monitor, &created,
			&monitor_created);
	index = 0;
	while (index < created)
		pthread_join(threads[index++], NULL);
	if (monitor_created)
		pthread_join(monitor, NULL);
	free(threads);
	sim_destroy(&sim);
	if (!result)
	{
		write(STDERR_FILENO, "codexion: failed to create threads\n",
			sizeof("codexion: failed to create threads\n") - 1);
		return (1);
	}
	return (0);
}
