/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memset.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/21 12:32:33 by adarabi           #+#    #+#             */
/*   Updated: 2026/04/29 17:33:29 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>

void	*ft_memset(void *ptr, int value, size_t size)
{
	unsigned char	*p;
	unsigned char	c;

	p = (unsigned char *)ptr;
	c = (unsigned char)value;
	while (size--)
	{
		*p = c;
		p++;
	}
	return (ptr);
}

// int main() {
//     char str[] = "Hello world!";
//     printf("%s\n", (char *)ft_memset(str, 'a', 4));
//     return 0;
// }
