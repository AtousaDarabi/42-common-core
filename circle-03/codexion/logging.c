#include "codexion.h"

#include <errno.h>
#include <sys/time.h>
#include <sys/types.h>
#include <unistd.h>

static size_t	append_number(char *buffer, size_t offset, long long number)
{
	char				digits[24];
	unsigned long long	value;
	size_t				count;

	value = (unsigned long long)number;
	count = 0;
	if (number < 0)
	{
		buffer[offset++] = '-';
		value = (unsigned long long)(-number);
	}
	while (value > 0)
	{
		digits[count++] = (char)('0' + value % 10);
		value /= 10;
	}
	if (count == 0)
		digits[count++] = '0';
	while (count > 0)
		buffer[offset++] = digits[--count];
	return (offset);
}

static int	write_line(const char *buffer, size_t length)
{
	ssize_t	written;

	while (length > 0)
	{
		written = write(STDOUT_FILENO, buffer, length);
		if (written < 0 && errno == EINTR)
			continue ;
		if (written <= 0)
			return (0);
		buffer += written;
		length -= (size_t)written;
	}
	return (1);
}

void	log_state(t_sim *sim, int coder_id, const char *message,
		long long timestamp)
{
	char	buffer[128];
	size_t	offset;
	size_t	index;

	offset = append_number(buffer, 0, timestamp);
	buffer[offset++] = ' ';
	offset = append_number(buffer, offset, coder_id);
	buffer[offset++] = ' ';
	index = 0;
	while (message[index] != '\0')
		buffer[offset++] = message[index++];
	buffer[offset++] = '\n';
	pthread_mutex_lock(&sim->log_mutex);
	if (!write_line(buffer, offset))
		write(STDERR_FILENO, "codexion: failed to write log\n",
			sizeof("codexion: failed to write log\n") - 1);
	pthread_mutex_unlock(&sim->log_mutex);
}

long long	time_now_ms(void)
{
	struct timeval	now;

	if (gettimeofday(&now, NULL) != 0)
		return (-1);
	return ((long long)now.tv_sec * 1000 + now.tv_usec / 1000);
}
