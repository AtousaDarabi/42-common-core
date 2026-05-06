/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memcpy.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/21 22:45:19 by adarabi           #+#    #+#             */
/*   Updated: 2026/05/07 00:25:41 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdlib.h>

void	*ft_memcpy(void *des, const void *src, size_t size)
{
	unsigned char		*d;
	const unsigned char	*s;

	if (!des && !src)
		return (NULL);
	d = (unsigned char *)des;
	s = (const unsigned char *)src;
	while (size--)
	{
		*d++ = *s++;
	}
	return (des);
}

// int main()
// {
//     char src[] = "Bravo! It works.";
//     char dest[20];
//     char *ret;

//     ret = ft_memcpy(dest, src, sizeof(src));

//     printf("Test 1\n");
//     printf("Source:      %s\n", src);
//     printf("Destination: %s\n", dest);
//     printf("Return ptr:  %p\n", ret);
//     printf("Dest ptr:    %p\n", (void *)dest);

//     if (ret == dest)
//         printf("Result: Return pointer is correct.\n\n");
//     else
//         printf("Result: Return pointer is WRONG.\n\n");

//     char src2[] = "123456789";
//     char dest2[] = "AAAAAAAAA";

//     printf("Test 2\n");
//     printf("Before: %s\n", dest2);

//     ft_memcpy(dest2, src2, 5);

//     printf("After:  %s\n", dest2); 

//     return 0;
// }
