/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/18 18:51:16 by adarabi           #+#    #+#             */
/*   Updated: 2026/05/18 22:09:23 by adarabi          ###   ########.fr       */
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
	str = malloc(sizeof(char) * (idx + 2));
	if (!str)
		return (0);
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
	char	*str;
	int		idx;
	int		idx2;

	idx = 0;
	idx2 = 0;
	while (s[idx] != 0 && s[idx] != '\n')
		idx++;
	if (!s[idx])
	{
		free(s);
		return (0);
	}
	str = malloc(sizeof(char) * (ft_strlen(s) - idx + 1));
	if (!str)
		return (0);
	idx++;
	while (s[idx] != 0)
		str[idx2++] = s[idx++];
	str[idx2] = 0;
	free(s);
	return (str);
}

char	*fileread(int fd, char *s)
{
	char	*buff;
	int		count;

	count = 999999;
	buff = malloc(sizeof(char) * BUFFER_SIZE + 1);
	if (!buff)
		return (0);
	while (!ft_chrfind(s, '\n') && count != 0)
	{
		count = read(fd, buff, BUFFER_SIZE);
		if (count == -1)
		{
			free(buff);
			return (0);
		}
		buff[count] = 0;
		s = ft_strjoin(s, buff);
	}
	free(buff);
	return (s);
}

char	*get_next_line(int fd)
{
	static char		*str[256];
	char			*first_line;

	if (fd < 0 || fd >= 256 || BUFFER_SIZE <= 0)
		return (0);
	str[fd] = fileread(fd, str[fd]);
	if (!str[fd])
		return (0);
	first_line = get_first_line(str[fd]);
	str[fd] = line_after(str[fd]);
	return (first_line);
}

// int main()
// {
// 	return 0;
// }
