/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memcpy.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/21 22:45:19 by adarabi           #+#    #+#             */
/*   Updated: 2026/05/12 16:07:02 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memcpy(void *des, const void *src, size_t size)
{
	unsigned char		*d;
	const unsigned char	*s;

	if (!des && !src)
		return (NULL);
	d = (unsigned char *)des;
	s = (const unsigned char *)src;
	while (size--)
		*d++ = *s++;
	return (des);
}
