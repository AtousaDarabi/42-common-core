/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strlcat.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/22 17:23:03 by adarabi           #+#    #+#             */
/*   Updated: 2026/05/12 16:04:53 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

size_t	ft_strlcat(char *str1, const char *str2, size_t size)
{
	size_t	len1;
	size_t	len2;
	size_t	i;

	len1 = 0;
	len2 = 0;
	i = 0;
	while (str1[len1] && len1 < size)
		len1++;
	while (str2[len2])
		len2++;
	if (len1 >= size)
		return (size + len2);
	while (str2[i] && (len1 + i) < (size - 1))
	{
		str1[len1 + i] = str2[i];
		i++;
	}
	str1[len1 + i] = '\0';
	return (len1 + len2);
}
