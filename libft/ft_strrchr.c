/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strrchr.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/23 10:43:34 by adarabi           #+#    #+#             */
/*   Updated: 2026/05/07 00:25:41 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdlib.h>

char	*ft_strrchr(const char *str, int c)
{
	const char	*last_occurrence;

	last_occurrence = NULL;
	while (*str != '\0')
	{
		if (*str == (char)c)
			last_occurrence = str;
		str++;
	}
	if (*str == (char)c)
		return ((char *)str);
	return ((char *)last_occurrence);
}

// int main()
// {
//     printf("%s",(char *)ft_strrchr("You come here cowboy.", 'c'));
//     return (0);
// }
