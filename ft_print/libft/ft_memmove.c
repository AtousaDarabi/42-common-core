/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memmove.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/21 23:22:31 by adarabi           #+#    #+#             */
/*   Updated: 2026/05/12 16:03:54 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memmove(void *des, const void *src, size_t size)
{
	unsigned char	*d;
	unsigned char	*s;

	if (!des && !src)
		return (NULL);
	if (des < src)
	{
		d = (unsigned char *)des;
		s = (unsigned char *)src;
		while (size--)
			*d++ = *s++;
	}
	else if (des > src)
	{
		d = (unsigned char *)des + size - 1;
		s = (unsigned char *)src + size - 1;
		while (size--)
			*d-- = *s--;
	}
	return (des);
}
