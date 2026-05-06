/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strmapi.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/29 19:55:09 by adarabi           #+#    #+#             */
/*   Updated: 2026/05/07 00:13:10 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"
#include <stdlib.h>
// #include <stdio.h>

char	*ft_strmapi(const char *s, char (*f)(unsigned int, char))
{
	char			*str;
	unsigned int	i;

	if (!s || !f)
		return (NULL);
	str = (char *)malloc(sizeof (char) * (ft_strlen((char *)s) + 1));
	if (!str)
		return (NULL);
	i = 0;
	while (s[i])
	{
		str[i] = f(i, s[i]);
		i++;
	}
	str[i] = '\0';
	return (str);
}

// char my_transformer(unsigned int i, char c)
// {
//     if (i % 2 == 0 && (c >= 'a' && c <= 'z'))
//         return (c - 32);
//     return (c);
// }

// char my_test_func(unsigned int i, char c)
// {
//     return (c + 1);
// }

// int main()
// {
//     char *res = ft_strmapi("abc", my_test_func);
//     printf("%s\n", res);
//     char *new_str = ft_strmapi("hello", my_transformer);
//     printf("%s\n", new_str);
// 	return (0);
// }
