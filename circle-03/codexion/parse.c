#include "codexion.h"

static int	is_number(const char *s)
{
	int	i;

	if (s[0] == '\0' || strlen(s) > 9)
		return (0);
	i = 0;
	while (s[i])
	{
		if (s[i] < '0' || s[i] > '9')
			return (0);
		i++;
	}
	return (1);
}

static void	fill_config(char **av, t_config *cfg)
{
	cfg->n = atoi(av[1]);
	cfg->t_burnout = atoi(av[2]);
	cfg->t_compile = atoi(av[3]);
	cfg->t_debug = atoi(av[4]);
	cfg->t_refactor = atoi(av[5]);
	cfg->n_compiles = atoi(av[6]);
	cfg->cooldown = atoi(av[7]);
}

static int	parse_sched(const char *s, t_sched *out)
{
	if (strcmp(s, "fifo") == 0)
		*out = SCHEDULER_FIFO;
	else if (strcmp(s, "edf") == 0)
		*out = SCHEDULER_EDF;
	else
		return (0);
	return (1);
}

static int	check_values(t_config *cfg)
{
	if (cfg->n < 1 || cfg->t_burnout < 1)
		return (error_msg("coders and burnout time must be >= 1"));
	if (cfg->t_compile < 1 || cfg->n_compiles < 1)
		return (error_msg("compile time and count must be >= 1"));
	return (0);
}

int	parse_args(int ac, char **av, t_config *cfg)
{
	int	i;

	if (ac != 9)
		return (error_msg("expected exactly 8 arguments"));
	i = 1;
	while (i < 8)
	{
		if (!is_number(av[i]))
			return (error_msg("numbers must be non-negative integers"));
		i++;
	}
	fill_config(av, cfg);
	if (!parse_sched(av[8], &cfg->sched))
		return (error_msg(SCHED_ERR_MSG));
	return (check_values(cfg));
}
