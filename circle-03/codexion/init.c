#include "codexion.h"

#include <stdlib.h>
#include <string.h>

static int	allocate_simulation(t_sim *sim)
{
	size_t	count;

	count = (size_t)sim->config.coder_count;
	if (count > (size_t)-1 / sizeof(*sim->coders)
		|| count > (size_t)-1 / sizeof(*sim->dongles)
		|| count > (size_t)-1 / sizeof(*sim->heap))
		return (0);
	sim->coders = malloc(count * sizeof(*sim->coders));
	if (sim->coders == NULL)
		return (0);
	memset(sim->coders, 0, count * sizeof(*sim->coders));
	sim->dongles = malloc(count * sizeof(*sim->dongles));
	if (sim->dongles == NULL)
		return (0);
	memset(sim->dongles, 0, count * sizeof(*sim->dongles));
	sim->heap = malloc(count * sizeof(*sim->heap));
	if (sim->heap == NULL)
		return (0);
	memset(sim->heap, 0, count * sizeof(*sim->heap));
	return (1);
}

static int	initialize_mutexes(t_sim *sim)
{
	int	index;

	if (pthread_mutex_init(&sim->mutex, NULL) != 0)
		return (0);
	sim->mutex_initialized = 1;
	if (pthread_mutex_init(&sim->log_mutex, NULL) != 0)
		return (0);
	sim->log_mutex_initialized = 1;
	if (pthread_cond_init(&sim->condition, NULL) != 0)
		return (0);
	sim->condition_initialized = 1;
	index = 0;
	while (index < sim->config.coder_count)
	{
		if (pthread_mutex_init(&sim->dongles[index].mutex, NULL) != 0)
			return (0);
		sim->dongles[index].initialized = 1;
		index++;
	}
	return (1);
}

static void	initialize_coders(t_sim *sim)
{
	int	index;

	index = 0;
	while (index < sim->config.coder_count)
	{
		sim->coders[index].sim = sim;
		sim->coders[index].id = index + 1;
		sim->coders[index].left = index;
		sim->coders[index].right = (index + 1) % sim->config.coder_count;
		sim->coders[index].last_compile_start = sim->start_ms;
		index++;
	}
}

int	sim_init(t_sim *sim, const t_config *config)
{
	memset(sim, 0, sizeof(*sim));
	sim->config = *config;
	sim->start_ms = time_now_ms();
	if (sim->start_ms < 0 || !allocate_simulation(sim))
		return (0);
	if (!initialize_mutexes(sim))
		return (0);
	initialize_coders(sim);
	return (1);
}

void	sim_destroy(t_sim *sim)
{
	int	index;

	index = 0;
	while (sim->dongles != NULL && index < sim->config.coder_count)
	{
		if (sim->dongles[index].initialized)
			pthread_mutex_destroy(&sim->dongles[index].mutex);
		index++;
	}
	if (sim->condition_initialized)
		pthread_cond_destroy(&sim->condition);
	if (sim->log_mutex_initialized)
		pthread_mutex_destroy(&sim->log_mutex);
	if (sim->mutex_initialized)
		pthread_mutex_destroy(&sim->mutex);
	free(sim->coders);
	free(sim->dongles);
	free(sim->heap);
}
