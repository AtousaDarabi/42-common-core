/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_calloc.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/27 19:26:23 by adarabi           #+#    #+#             */
/*   Updated: 2026/04/29 17:30:40 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"
#include <stdio.h>
#include <stdlib.h>

void	*ft_calloc(size_t mem_count, size_t size)
{
	size_t	total;
	void	*ptr;

	total = mem_count * size;
	ptr = malloc(total);
	if (ptr == NULL)
		return (NULL);
	ft_memset(ptr, 0, total);
	return (ptr);
}

// int main ()
// {
//     int *arr;
//     arr = (int *)calloc(5, sizeof(int));
//     if (arr == NULL)
//         return (1);
//     free(arr);
// }
