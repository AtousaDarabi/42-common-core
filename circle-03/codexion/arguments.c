#include "codexion.h"

#include <limits.h>
#include <string.h>

static int	parse_number(const char *text, int *number)
{
	long	value;
	int		digit;

	if (*text == '\0')
		return (0);
	value = 0;
	while (*text != '\0')
	{
		if (*text < '0' || *text > '9')
			return (0);
		digit = *text - '0';
		if (value > (INT_MAX - digit) / 10)
			return (0);
		value = value * 10 + digit;
		text++;
	}
	*number = (int)value;
	return (1);
}

int	parse_arguments(int argc, char **argv, t_config *config)
{
	int	values[7];
	int	index;

	if (argc != 9)
		return (0);
	index = 0;
	while (index < 7)
	{
		if (!parse_number(argv[index + 1], &values[index]))
			return (0);
		index++;
	}
	config->coder_count = values[0];
	config->burnout_ms = values[1];
	config->compile_ms = values[2];
	config->debug_ms = values[3];
	config->refactor_ms = values[4];
	config->required_compiles = values[5];
	config->cooldown_ms = values[6];
	if (config->coder_count < 1 || config->burnout_ms < 1
		|| config->compile_ms < 1 || config->debug_ms < 1
		|| config->refactor_ms < 1 || config->cooldown_ms < 1)
		return (0);
	if (strcmp(argv[8], "fifo") == 0)
		config->scheduler = FIFO;
	else if (strcmp(argv[8], "edf") == 0)
		config->scheduler = EDF;
	else
		return (0);
	return (1);
}
