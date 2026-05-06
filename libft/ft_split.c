/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_split.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/29 22:06:11 by adarabi           #+#    #+#             */
/*   Updated: 2026/05/07 00:53:33 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static int	ft_count_words(const char *s, char c)
{
	int	count;
	int	i;

	count = 0;
	i = 0;
	while (s[i])
	{
		while (s[i] && s[i] == c)
			i++;
		if (s[i])
			count++;
		while (s[i] && s[i] != c)
			i++;
	}
	return (count);
}

static char	**ft_free_all(char **str, int i)
{
	while (i >= 0)
	{
		free (str[i]);
		i--;
	}
	free (str);
	return (NULL);
}

static char	**ft_fill_split(char **res, const char *s, char c)
{
	size_t	i;
	size_t	j;
	size_t	word_start;

	i = 0;
	j = 0;
	while (s[i])
	{
		while (s[i] && s[i] == c)
			i++;
		if (s[i])
		{
			word_start = i;
			while (s[i] && s[i] != c)
				i++;
			res[j] = ft_substr(s, word_start, i - word_start);
			if (!res[j])
				return (ft_free_all(res, j));
			j++;
		}
	}
	res[j] = NULL;
	return (res);
}

char	**ft_split(const char *s, char c)
{
	char	**res;

	if (!s)
		return (NULL);
	res = malloc(sizeof(char *) * (ft_count_words(s, c) + 1));
	if (!res)
		return (NULL);
	return (ft_fill_split(res, s, c));
}

// int	main(void)
// {
// 	char	**result;
// 	int		i;

// 	i = 0;
// 	result = ft_split(" Hi Atousa :) ", ' ');
// 	if (!result)
// 	{
// 		printf("Malloc failed!\n");
// 		return (1);
// 	}
// 	while (result[i] != NULL)
// 	{
// 		printf("Word [%d]: %s\n", i, result[i]);
// 		free(result[i]);
// 		i++;
// 	}
// 	free(result);
// 	return (0);
// }
