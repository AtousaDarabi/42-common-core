/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strlcpy.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/22 15:01:48 by adarabi           #+#    #+#             */
/*   Updated: 2026/05/07 00:25:41 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdlib.h>

size_t	ft_strlcpy(char *des, const char *src, size_t size)
{
	size_t	len;
	size_t	i;

	len = 0;
	i = 0;
	while (src[len] != '\0')
		len++;
	if (size == 0)
		return (len);
	while (src[i] != '\0' && i < (size - 1))
	{
		des[i] = src[i];
		i++;
	}
	des[i] = '\0';
	return (len);
}

// int main()
// {
//     char dest[10];
//     // Test 1: Normal copy
//     // Should copy "Hello", leaving room for \0
//     ft_strlcpy(dest, "Hello", 10);
//     printf("Test 1 (Normal): '%s' (Length: 5)\n", dest);
//     // Test 2: Truncation
//     // Copying "123456789" into a buffer of size 5
//     // Should only copy "1234" and add '\0'
//     size_t ret = ft_strlcpy(dest, "123456789", 5);
//     printf("Test 2 (Truncate): '%s' (Return: %zu)\n", dest, ret);
//     // Test 3: Size 0
//     // Should not write anything, just return source length
//     char empty[5] = "AAAA";
//     size_t ret2 = ft_strlcpy(empty, "Test", 0);
//     printf("Test 3 (Size 0): '%s' (Return: %zu)\n", empty, ret2);
//     return (0);
// }
