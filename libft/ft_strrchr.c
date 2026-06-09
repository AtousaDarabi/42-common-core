/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strrchr.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/23 10:43:34 by adarabi           #+#    #+#             */
/*   Updated: 2026/05/07 18:44:04 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strrchr(const char *str, int c)
{
	const char		*last;
	unsigned char	ch;

	last = NULL;
	ch = (unsigned char)c;
	while (*str != '\0')
	{
		if ((unsigned char)*str == ch)
			last = str;
		str++;
	}
	if (ch == '\0')
		return ((char *)str);
	return ((char *)last);
}

// int main()
// {
//     printf("%s",(char *)ft_strrchr("You come here cowboy.", 'c'));
//     return (0);
// }
