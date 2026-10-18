#include "codexion.h"

int	error_msg(const char *msg)
{
	fprintf(stderr, "Error: %s\n", msg);
	return (1);
}
