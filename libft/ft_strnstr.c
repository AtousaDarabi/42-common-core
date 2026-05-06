/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strnstr.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/24 03:22:42 by adarabi           #+#    #+#             */
/*   Updated: 2026/05/07 00:25:41 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdlib.h>

char	*ft_strnstr(const char *str, const char *substr, size_t len)
{
	size_t	i;
	size_t	j;

	if (*substr == '\0')
		return ((char *)str);
	i = 0;
	while (i < len && str[i] != '\0')
	{
		j = 0;
		while (str[i + j] == substr[j] && substr[j] != '\0' && (i + j) < len)
			j++;
		if (substr[j] == '\0')
			return ((char *)str + i);
		i++;
	}
	return (NULL);
}

// int main()
// {
//     char *str;
//     str = "How are you?";
//     char *substr;
//     substr = "are";
//     printf("%s", ft_strnstr(str, substr, 7));
//     return (0);
// }
