/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_bzero.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/21 21:14:59 by adarabi           #+#    #+#             */
/*   Updated: 2026/05/07 00:53:33 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	ft_bzero(void *ptr, size_t size)
{
	ft_memset(ptr, 0, size);
}

// int main()
// {
//     char str[] = "Hello!";
//     size_t n = 3;

//     printf("Before bzero: %s\n", str);

//     ft_bzero(str, n);

//     printf("After bzero (first 6 chars as numbers):\n");
//     for (int i = 0; i < 6; i++)
//     {
//         // 0 means it worked!
//         printf("Index %d: %d\n", i, str[i]);
//     }

//     return 0;
// }
