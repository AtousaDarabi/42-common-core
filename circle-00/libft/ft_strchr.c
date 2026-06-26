/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strchr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/22 18:22:05 by adarabi           #+#    #+#             */
/*   Updated: 2026/05/07 18:45:37 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strchr(const char *s, int c)
{
	unsigned char	ch;

	ch = (unsigned char)c;
	while (*s != '\0')
	{
		if ((unsigned char)*s == ch)
			return ((char *)s);
		s++;
	}
	if (ch == '\0')
		return ((char *)s);
	return (NULL);
}

// int main()
// {
//     char *str;
//     str = "";
//     printf("%s", ft_strchr(str, 'g'));
//     return (0);
// }

// char *my_strchr(const char *s, int c) {
//     // Loop until the end of the string
//     while (*s != (char)c) {
//         if (*s == '\0') {
//             return NULL; // Character not found before end of string
//         }
//         s++;
//     }
//     return (char *)s; // Found it, return the pointer
// }
