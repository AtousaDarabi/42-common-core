/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strncmp.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/23 11:27:05 by adarabi           #+#    #+#             */
/*   Updated: 2026/05/06 23:59:24 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>

int	ft_strncmp(const char *str1, const char *str2, size_t n)
{
	size_t	i;

	i = 0;
	if (n == 0)
		return (0);
	while (str1[i] && str1[i] == str2[i] && i < n - 1)
	{
		i++;
	}
	return ((unsigned char)str1[i] - (unsigned char)str2[i]);
}

// int main()
// {
//     char *str1 = "Hello!";
//     char *str2 = "How are you?";
//     printf("%d\n", ft_strncmp(str1, str2, 3));
// 	printf("%d\n", ft_strncmp("test\200", "test\0", 6));
//     return (0);
// }
