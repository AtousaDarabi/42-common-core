#ifndef CODEXION_H
# define CODEXION_H

# include <pthread.h>
# include <stdio.h>
# include <stdlib.h>
# include <string.h>
# include <sys/time.h>
# include <time.h>
# include <unistd.h>

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
	long	seq;
}	t_req;

/* Min-heap ordered by (key, seq). fifo: key = 0, edf: key = deadline. */
typedef struct s_heap
{
	t_req	*arr;
	int		size;
	int		cap;
	long	next_seq;
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
	t_dongle		*dongles;
	t_coder			*coders;
}	t_data;

/* main.c */
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

/* heap.c */
int		heap_init(t_heap *h, int cap);
void	heap_free(t_heap *h);
int		heap_push(t_heap *h, int coder_id, long key);
int		heap_peek(t_heap *h, t_req *out);
int		heap_pop(t_heap *h, t_req *out);

/* heap_ops.c */
int		req_less(t_req *a, t_req *b);
void	sift_up(t_heap *h, int i);
void	sift_down(t_heap *h, int i);

/* dongle_init.c */
int		dongle_init(t_data *d);
void	dongle_destroy(t_data *d, int count);

/* dongle_wait.c */
int		dongle_wait(t_coder *c, t_dongle *dg);

/* dongle.c */
int		dongle_acquire(t_coder *c, t_dongle *dg);
void	dongle_release(t_coder *c, t_dongle *dg);
void	dongle_wake_all(t_data *d);

/* coder_init.c */
int		init_coders(t_data *d);
void	destroy_coders(t_data *d, int count);

/* coder_utils.c */
void	sleep_ms(t_data *d, long ms);
int		take_dongles(t_coder *c);
void	release_dongles(t_coder *c);

/* coder.c */
void	*coder_routine(void *arg);

/* run.c */
int		start_threads(t_data *d);
void	join_threads(t_data *d, int count);
int		run_simulation(t_data *d);

/* monitor.c */
void	*monitor_routine(void *arg);

/* setup.c */
int		sim_init(t_data *d);
void	sim_destroy(t_data *d);

#endif
