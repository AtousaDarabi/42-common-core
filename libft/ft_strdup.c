/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strdup.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/28 14:48:03 by adarabi           #+#    #+#             */
/*   Updated: 2026/05/07 00:53:33 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strdup(const char *str)
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
