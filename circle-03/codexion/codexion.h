#ifndef CODEXION_H
# define CODEXION_H

# include <pthread.h>
# include <stddef.h>

typedef enum e_scheduler
{
	FIFO,
	EDF
}	t_scheduler;

typedef struct s_config
{
	int				coder_count;
	int				burnout_ms;
	int				compile_ms;
	int				debug_ms;
	int				refactor_ms;
	int				required_compiles;
	int				cooldown_ms;
	t_scheduler		scheduler;
}	t_config;

typedef struct s_sim	t_sim;

typedef struct s_dongle
{
	pthread_mutex_t	mutex;
	long long		available_at;
	int				held;
	int				initialized;
}	t_dongle;

typedef struct s_coder
{
	t_sim			*sim;
	int				id;
	int				left;
	int				right;
	int				compile_count;
	int				queued;
	int				granted;
	long long		last_compile_start;
}	t_coder;

typedef struct s_request
{
	int				coder_index;
	unsigned long long	order;
	long long		deadline;
}	t_request;

typedef struct s_sim
{
	t_config		config;
	t_coder			*coders;
	t_dongle		*dongles;
	t_request		*heap;
	size_t			heap_size;
	unsigned long long	next_order;
	pthread_mutex_t	mutex;
	pthread_mutex_t	log_mutex;
	pthread_cond_t	condition;
	int				mutex_initialized;
	int				log_mutex_initialized;
	int				condition_initialized;
	int				stop;
	long long		start_ms;
}	t_sim;

int				parse_arguments(int argc, char **argv, t_config *config);
int				sim_init(t_sim *sim, const t_config *config);
void			sim_destroy(t_sim *sim);
long long		time_now_ms(void);
void			log_state(t_sim *sim, int coder_id, const char *message,
					long long timestamp);
int				heap_push(t_sim *sim, int coder_index);
int				heap_remove(t_sim *sim, size_t index);
int				request_dongles(t_coder *coder);
void			dispatch_requests(t_sim *sim, long long now);
void			*run_coder(void *argument);
void			*run_monitor(void *argument);
void			stop_simulation(t_sim *sim);

#endif
