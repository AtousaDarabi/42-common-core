#include "codexion.h"

static int	init_one_coder(t_data *d, int i)
{
	t_coder	*c;

	c = &d->coders[i];
	c->id = i + 1;
	c->data = d;
	c->compiles = 0;
	c->last_compile_start = 0;
	c->left = &d->dongles[i];
	c->right = &d->dongles[(i + 1) % d->cfg.n];
	return (pthread_mutex_init(&c->lock, NULL));
}

int	init_coders(t_data *d)
{
	int	i;

	d->coders = malloc(sizeof(t_coder) * d->cfg.n);
	if (!d->coders)
		return (1);
	memset(d->coders, 0, sizeof(t_coder) * d->cfg.n);
	i = 0;
	while (i < d->cfg.n)
	{
		if (init_one_coder(d, i))
		{
			destroy_coders(d, i);
			return (1);
		}
		i++;
	}
	return (0);
}

void	destroy_coders(t_data *d, int count)
{
	int	i;

	i = 0;
	while (i < count)
	{
		pthread_mutex_destroy(&d->coders[i].lock);
		i++;
	}
	free(d->coders);
	d->coders = NULL;
}
