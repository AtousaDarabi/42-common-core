#include "codexion.h"

int	main(int argc, char **argv)
{
	t_data	data;

	memset(&data, 0, sizeof(data));
	if (parse_args(argc, argv, &data.cfg))
		return (1);
	printf("config OK: %d coders\n", data.cfg.n);
	return (0);
}
