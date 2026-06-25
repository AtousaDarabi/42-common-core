/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   flags.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/23 18:10:04 by adarabi           #+#    #+#             */
/*   Updated: 2026/06/23 18:10:08 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	check_flags(char *arg, t_bench *b, int *mode)
{
	if (!arg || arg[0] != '-' || arg[1] != '-')
		return (0);
	if (arg[2] == 'b')
	{
		b->active = 1;
		return (1);
	}
	if (arg[2] == 's')
		*mode = 1;
	else if (arg[2] == 'm')
		*mode = 2;
	else if (arg[2] == 'c')
		*mode = 3;
	else if (arg[2] == 'a')
		*mode = 4;
	else
		return (0);
	return (1);
}
