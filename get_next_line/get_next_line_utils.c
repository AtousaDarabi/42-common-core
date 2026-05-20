/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line_utils.c                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/18 18:52:00 by adarabi           #+#    #+#             */
/*   Updated: 2026/05/20 22:12:27 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

size_t	ft_strlen(char *str)
{
	size_t	count;

	count = 0;
	while (str[count])
		count++;
	return (count);
}

char	*ft_strjoin(char *s1, size_t len_s1, char *s2, size_t len_s2)
{
	char	*res;
	size_t	i;
	size_t	j;

	res = malloc(len_s1 + len_s2 + 1);
	if (!res)
		return (free(s1), NULL);
	i = 0;
	if (s1)
	{
		while (i < len_s1)
		{
			res[i] = s1[i];
			i++;
		}
	}
	j = 0;
	while (j < len_s2)
		res[i++] = s2[j++];
	res[i] = '\0';
	return (free(s1), res);
}

char	*alloc_after(char *s, int idx)
{
	char	*str;
	int		i;

	str = malloc(sizeof(char) * (ft_strlen(s) - idx + 1));
	if (!str)
	{
		free(s);
		return (NULL);
	}
	i = 0;
	idx++;
	while (s[idx])
		str[i++] = s[idx++];
	str[i] = '\0';
	free(s);
	return (str);
}

char	*do_read(int fd, char **s, char *buff, size_t *len)
{
	int	count;

	count = read(fd, buff, BUFFER_SIZE);
	if (count == -1)
	{
		free(*s);
		*s = NULL;
		return (NULL);
	}
	if (count == 0)
		return (*s);
	buff[count] = '\0';
	*s = ft_strjoin(*s, *len, buff, count);
	*len += count;
	return (*s);
}

int	ft_chrfind(char *str, int c)
{
	int	idx;

	if (!str)
		return (0);
	idx = 0;
	if (c == '\0')
		return (0);
	while (str[idx] != 0)
	{
		if (str[idx] == (char)c)
			return (1);
		idx++;
	}
	return (0);
}
