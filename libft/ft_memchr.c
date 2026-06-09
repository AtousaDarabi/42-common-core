/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memchr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/23 12:21:35 by adarabi           #+#    #+#             */
/*   Updated: 2026/05/07 00:53:33 by adarabi          ###   ########.fr       */
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

// int main()
// {
//     char data[] = {'A', 'B', '\0', 'C', 'Z', 'E'};
//     size_t size = 6;
//     printf("Searching in buffer: A, B, \\0, C, Z, E\n\n");
//     char *res1 = ft_memchar(data, 'Z', size);
//     if (res1)
//         printf("Test 1 (Find 'Z'): Success! Found at index %ld\n",
// 					 res1 - data);
//     else
//         printf("Test 1 (Find 'Z'): Failed!\n");
//     char *res2 = ft_memchar(data, '\0', size);
//     if (res2)
//         printf("Test 2 (Find '\\0'): Success! Found at index %ld\n",
// 					 res2 - data);
//     char *res3 = ft_memchar(data, 'X', size);
//     if (res3 == NULL)
//         printf("Test 3 (Find 'X'): Success! Returned NULL as expected.\n");
//     return (0);
// }
