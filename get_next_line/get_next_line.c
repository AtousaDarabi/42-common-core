/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/18 18:51:16 by adarabi           #+#    #+#             */
/*   Updated: 2026/05/27 15:19:07 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

char	*get_first_line(char *s)
{
	char	*str;
	int		idx;

	idx = 0;
	while (s[idx] && s[idx] != '\n')
		idx++;
	str = malloc(sizeof(char) * (idx + (s[idx] == '\n') + 1));
	if (!str)
		return (NULL);
	idx = 0;
	while (s[idx] && s[idx] != '\n')
	{
		str[idx] = s[idx];
		idx++;
	}
	if (s[idx] == '\n')
		str[idx++] = '\n';
	str[idx] = 0;
	return (str);
}

char	*line_after(char *s)
{
	int	idx;

	idx = 0;
	while (s[idx] && s[idx] != '\n')
		idx++;
	if (!s[idx])
	{
		free(s);
		return (NULL);
	}
	return (alloc_after(s, idx));
}

static char	*read_loop(int fd, char *s, char *buff)
{
	size_t	len;

	len = 0;
	if (s)
		len = ft_strlen(s);
	while (1)
	{
		buff[0] = '\0';
		if (!do_read(fd, &s, buff, &len))
			return (NULL);
		if (buff[0] == '\0')
			break ;
		if (ft_chrfind(buff, '\n'))
			break ;
	}
	return (s);
}

char	*file_read(int fd, char *s)
{
	char	*buff;

	buff = malloc(BUFFER_SIZE + 1);
	if (!buff)
	{
		free(s);
		return (NULL);
	}
	s = read_loop(fd, s, buff);
	free(buff);
	return (s);
}

char	*get_next_line(int fd)
{
	static char	*str[4096];
	char		*first_line;

	if (fd < 0 || fd >= 4096 || BUFFER_SIZE <= 0)
		return (NULL);
	str[fd] = file_read(fd, str[fd]);
	if (!str[fd] || !str[fd][0])
	{
		free(str[fd]);
		str[fd] = NULL;
		return (NULL);
	}
	first_line = get_first_line(str[fd]);
	if (!first_line)
	{
		free(str[fd]);
		str[fd] = NULL;
		return (NULL);
	}
	str[fd] = line_after(str[fd]);
	return (first_line);
}

// #include <fcntl.h>
// #include <stdio.h>

// int main(void)
// {
//     int     fd;
//     char    *line;

//     fd = open("file-one.txt", O_RDONLY);
//     if (fd < 0)
//         return (1);
//     while ((line = get_next_line(fd)) != NULL)
//     {
//         printf("%s", line);
//         free(line);
//     }
//     close(fd);
//     return (0);
// }
