/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strjoin.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/28 18:45:26 by adarabi           #+#    #+#             */
/*   Updated: 2026/04/29 18:16:03 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"
#include <stdio.h>
#include <stdlib.h>

char	*ft_strjoin(char const *s1, char const *s2)
{
	size_t	total_len;
	char	*str;
	char	*str_final;

	total_len = ft_strlen((char *)s1) + ft_strlen((char *)s2);
	str = (char *)malloc(sizeof(char) * (total_len + 1));
	if (!str)
		return (NULL);
	str_final = str;
	while (*s1)
		*str_final++ = *s1++;
	while (*s2)
		*str_final++ = *s2++;
	*str_final = '\0';
	return (str);
}

// int main()
// {
//     printf("%s", ft_strjoin("Hi", " Atousa"));
//     return (0);
// }
