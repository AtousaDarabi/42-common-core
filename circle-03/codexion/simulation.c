#include "codexion.h"

#include <errno.h>
#include <time.h>
#include <unistd.h>

static void	make_deadline(struct timespec *deadline, long long time_ms)
{
	deadline->tv_sec = (time_t)(time_ms / 1000);
	deadline->tv_nsec = (long)(time_ms % 1000) * 1000000L;
}

static int	sleep_phase(t_sim *sim, long long duration)
{
	long long		end;
	long long		now;
	struct timespec	deadline;
	int				result;

	pthread_mutex_lock(&sim->mutex);
	end = time_now_ms() + duration;
	while (!sim->stop)
	{
		now = time_now_ms();
		if (now >= end)
			break ;
		make_deadline(&deadline, end);
		result = pthread_cond_timedwait(&sim->condition, &sim->mutex,
				&deadline);
		if (result != 0 && result != ETIMEDOUT)
		{
			sim->stop = 1;
			pthread_cond_broadcast(&sim->condition);
		}
	}
	result = !sim->stop;
	pthread_mutex_unlock(&sim->mutex);
	return (result);
}

static void	release_dongles(t_sim *sim, t_coder *coder, long long now)
{
	int	first;
	int	second;

	first = coder->left;
	second = coder->right;
	if (first > second)
	{
		first = coder->right;
		second = coder->left;
	}
	pthread_mutex_lock(&sim->dongles[first].mutex);
	if (second != first)
		pthread_mutex_lock(&sim->dongles[second].mutex);
	sim->dongles[coder->left].held = 0;
	sim->dongles[coder->left].available_at = now + sim->config.cooldown_ms;
	if (coder->right != coder->left)
	{
		sim->dongles[coder->right].held = 0;
		sim->dongles[coder->right].available_at = now
			+ sim->config.cooldown_ms;
	}
	if (second != first)
		pthread_mutex_unlock(&sim->dongles[second].mutex);
	pthread_mutex_unlock(&sim->dongles[first].mutex);
}

static int	finish_compile(t_coder *coder)
{
	t_sim		*sim;
	long long	now;

	sim = coder->sim;
	pthread_mutex_lock(&sim->mutex);
	if (sim->stop)
	{
		pthread_mutex_unlock(&sim->mutex);
		return (0);
	}
	now = time_now_ms();
	release_dongles(sim, coder, now);
	coder->compile_count++;
	log_state(sim, coder->id, "is debugging", now - sim->start_ms);
	pthread_cond_broadcast(&sim->condition);
	dispatch_requests(sim, now);
	pthread_mutex_unlock(&sim->mutex);
	return (1);
}

static int	begin_refactoring(t_coder *coder)
{
	t_sim		*sim;
	long long	now;

	sim = coder->sim;
	pthread_mutex_lock(&sim->mutex);
	if (sim->stop)
	{
		pthread_mutex_unlock(&sim->mutex);
		return (0);
	}
	now = time_now_ms();
	log_state(sim, coder->id, "is refactoring", now - sim->start_ms);
	pthread_mutex_unlock(&sim->mutex);
	return (1);
}

void	*run_coder(void *argument)
{
	t_coder	*coder;
	t_sim	*sim;

	coder = argument;
	sim = coder->sim;
	while (request_dongles(coder))
	{
		if (!sleep_phase(sim, sim->config.compile_ms)
			|| !finish_compile(coder)
			|| !sleep_phase(sim, sim->config.debug_ms)
			|| !begin_refactoring(coder)
			|| !sleep_phase(sim, sim->config.refactor_ms))
			break ;
	}
	return (NULL);
}

static int	all_coders_finished(t_sim *sim)
{
	int	index;

	index = 0;
	while (index < sim->config.coder_count)
	{
		if (sim->coders[index].compile_count < sim->config.required_compiles)
			return (0);
		index++;
	}
	return (1);
}

void	*run_monitor(void *argument)
{
	t_sim			*sim;
	long long		now;
	long long		deadline_ms;
	struct timespec	deadline;
	int				index;
	int				result;

	sim = argument;
	pthread_mutex_lock(&sim->mutex);
	while (!sim->stop)
	{
		if (all_coders_finished(sim))
		{
			sim->stop = 1;
			pthread_cond_broadcast(&sim->condition);
			break ;
		}
		now = time_now_ms();
		index = 0;
		while (index < sim->config.coder_count && !sim->stop)
		{
			deadline_ms = sim->coders[index].last_compile_start
				+ sim->config.burnout_ms;
			if (now >= deadline_ms)
			{
				sim->stop = 1;
				log_state(sim, sim->coders[index].id, "burned out",
					deadline_ms - sim->start_ms);
				pthread_cond_broadcast(&sim->condition);
			}
			index++;
		}
		if (sim->stop)
			break ;
		make_deadline(&deadline, now + 1);
		result = pthread_cond_timedwait(&sim->condition, &sim->mutex,
				&deadline);
		if (result != 0 && result != ETIMEDOUT)
		{
			sim->stop = 1;
			write(STDERR_FILENO, "codexion: monitor wait failed\n",
				sizeof("codexion: monitor wait failed\n") - 1);
			pthread_cond_broadcast(&sim->condition);
		}
	}
	pthread_mutex_unlock(&sim->mutex);
	return (NULL);
}

void	stop_simulation(t_sim *sim)
{
	pthread_mutex_lock(&sim->mutex);
	sim->stop = 1;
	pthread_cond_broadcast(&sim->condition);
	pthread_mutex_unlock(&sim->mutex);
}
