/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strdup.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/28 14:48:03 by adarabi           #+#    #+#             */
/*   Updated: 2026/04/29 18:43:28 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"
#include <stdlib.h>

char	*ft_strdup(char *str)
{
	char	*start;
	char	*dest;

	dest = (char *)malloc(ft_strlen(str) + 1);
	if (!dest)
		return (NULL);
	start = dest;
	while (*str)
		*dest++ = *str++;
	*dest = '\0';
	return (start);
}

// int main()
// {
//     printf("%s", ft_strdup("Hello Atousa"));
//     return (0);
// }
