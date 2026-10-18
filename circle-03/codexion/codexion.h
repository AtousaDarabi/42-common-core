#ifndef CODEXION_H
# define CODEXION_H

# include <pthread.h> // pthread_mutex_t | pthread_cond_t
# include <stdio.h> // stderr
# include <stdlib.h> // atoi
# include <string.h> // memset
# include <sys/time.h> //gettimeofday
// # include <unistd.h>

# define SCHED_ERR_MSG "scheduler must be exactly fifo or edf"

typedef enum e_sched
{
	SCHEDULER_FIFO,
	SCHEDULER_EDF
}	t_sched;

/* Everything that comes from the command line. */
typedef struct s_config
{
	int		n;
	long	t_burnout;
	long	t_compile;
	long	t_debug;
	long	t_refactor;
	int		n_compiles;
	long	cooldown;
	t_sched	sched;
}	t_config;

/* One waiting request inside a dongle queue. */
typedef struct s_req
{
	int		coder_id;
	long	key;
}	t_req;

/* Min-heap: key = arrival time (fifo) or deadline (edf). */
typedef struct s_heap
{
	t_req	*arr;
	int		size;
	int		cap;
}	t_heap;

typedef struct s_dongle
{
	pthread_mutex_t	mutex;
	pthread_cond_t	cond;
	int				in_use;
	long			free_at;
	t_heap			queue;
}	t_dongle;

typedef struct s_coder
{
	int				id;
	pthread_t		thread;
	pthread_mutex_t	lock;
	long			last_compile_start;
	int				compiles;
	t_dongle		*left;
	t_dongle		*right;
	struct s_data	*data;
}	t_coder;

typedef struct s_data
{
	t_config		cfg;
	long			start_ms;
	int				stop;
	pthread_mutex_t	stop_mutex;
	pthread_mutex_t	log_mutex;
	// t_dongle		*dongles;
	t_coder			*coders;
}	t_data;

/* error.c */
int		error_msg(const char *msg);

/* parse.c */
int		parse_args(int ac, char **av, t_config *cfg);

/* utils.c */
long	get_time_ms(void);
long	elapsed_ms(t_data *d);
int		is_stopped(t_data *d);
void	set_stop(t_data *d);

/* log.c */
void	print_state(t_coder *c, const char *msg);
void	print_burnout(t_data *d, int id);

#endif
