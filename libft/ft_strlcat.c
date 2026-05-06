/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strlcat.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/22 17:23:03 by adarabi           #+#    #+#             */
/*   Updated: 2026/04/29 17:00:27 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>

size_t	ft_strlcat(char *str1, const char *str2, size_t size)
{
	size_t	len1;
	size_t	len2;
	size_t	i;

	len1 = 0;
	len2 = 0;
	i = 0;
	while (str1[len1] && len1 < size)
		len1++;
	while (str2[len2])
		len2++;
	if (len1 >= size)
		return (size + len2);
	while (str2[i] && (len1 + i) < (size - 1))
	{
		str1[len1 + i] = str2[i];
		i++;
	}
	str1[len1 + i] = '\0';
	return (len1 + len2);
}

// int main()
// {
//     // Plenty of space
//     char dst1[20] = "Hello";
//     size_t ret1 = ft_strlcat(dst1, " World", 20);
//     printf("Scenario 1 (Fits):\n\tString: '%s'\n\tReturn: %zu\n\n",
//				 dst1, ret1);
//     // Truncation (Not enough space)
//     // Buffer size is 9. "Hello" (5) + " World" (6) = 11. 
//     // It will be cut off to fit in 9 bytes total.
//     char dst2[9] = "Hello";
//     size_t ret2 = ft_strlcat(dst2, " World", 9);
//     printf("Scenario 2 (Truncate):\n\tString: '%s'\n\tReturn: %zu\n\n",
//				 dst2, ret2);
//     // Destination already full
//     // size is 5, but "Hello" is 5. Nothing will be appended.
//     char dst3[5] = "Hello";
//     size_t ret3 = ft_strlcat(dst3, " World", 5);
//     printf("Scenario 3 (Full):\n\tString: '%s'\n\tReturn: %zu\n",
//    			 dst3, ret3);
//     return (0);
// }
