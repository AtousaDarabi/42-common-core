#include "codexion.h"

/* Sleeps ms milliseconds but wakes up early if the simulation stops. */
void	sleep_ms(t_data *d, long ms)
{
	long	end;

	end = get_time_ms() + ms;
	while (!is_stopped(d) && get_time_ms() < end)
		usleep(1000);
}

/* Only one dongle exists: take it once, then wait for the end. */
static int	lone_coder(t_coder *c)
{
	if (dongle_acquire(c, c->left))
		return (1);
	print_state(c, "has taken a dongle");
	while (!is_stopped(c->data))
		usleep(1000);
	dongle_release(c, c->left);
	return (1);
}

/* Returns 0 with both dongles held, 1 if the simulation stopped. */
int	take_dongles(t_coder *c)
{
	t_dongle	*first;
	t_dongle	*second;

	if (c->left == c->right)
		return (lone_coder(c));
	first = c->left;
	second = c->right;
	if (second < first)
	{
		first = c->right;
		second = c->left;
	}
	if (dongle_acquire(c, first))
		return (1);
	print_state(c, "has taken a dongle");
	if (dongle_acquire(c, second))
	{
		dongle_release(c, first);
		return (1);
	}
	print_state(c, "has taken a dongle");
	return (0);
}

void	release_dongles(t_coder *c)
{
	dongle_release(c, c->left);
	dongle_release(c, c->right);
}
