/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_atoi.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jukohler <jukohler@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/12 17:01:44 by jukohler          #+#    #+#             */
/*   Updated: 2026/06/12 17:07:10 by jukohler         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

int	ft_atoi(char *str, int *error)
{
	long	num;
	int		sign;
	char	*start;

	num = 0;
	sign = 1;
	start = str;
	if (*str == '-' || *str == '+')
		if (*str++ == '-')
			sign = -1;
	if (!*str)
		return (*error = 1, 0);
	while (*str && *str >= '0' && *str <= '9')
	{
		num = num * 10 + (*str++ - '0');
		if (num > 2147483648 || (sign == 1 && num > 2147483647))
			return (*error = 1, 0);
	}
	if (*str != '\0' || start == str || *(str - 1) == '-' || *(str - 1) == '+')
		return (*error = 1, 0);
	return ((int)(num * sign));
}
