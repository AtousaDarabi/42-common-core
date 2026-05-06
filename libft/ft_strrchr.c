/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strrchr.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/23 10:43:34 by adarabi           #+#    #+#             */
/*   Updated: 2026/05/07 00:01:47 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>

char	*ft_strrchr(const char *str, int c)
{
	char	*start;

	start = str;
	if (*str == '\0')
	{
		if (c == '\0')
			return ((char *)str);
		return (NULL);
	}
	while (*str != '\0')
		str++;
	while (str >= start)
	{
		if (*str == c)
			return ((char *)str);
		else
			str--;
	}
	return (NULL);
}

// int main()
// {
//     printf("%s",(char *)ft_strrchr("You come here cowboy.", 'c'));
//     return (0);
// }
