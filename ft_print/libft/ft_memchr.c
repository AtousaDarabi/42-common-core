/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memchr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/23 12:21:35 by adarabi           #+#    #+#             */
/*   Updated: 2026/05/12 16:03:40 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memchr(const void *ptr, int value, size_t n)
{
	const unsigned char	*str;
	unsigned char		val;

	str = (const unsigned char *)ptr;
	val = (unsigned char)value;
	while (n--)
	{
		if (*str == val)
			return ((void *)str);
		str++;
	}
	return (NULL);
}
