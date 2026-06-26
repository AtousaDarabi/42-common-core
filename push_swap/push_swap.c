/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/23 18:09:00 by jukohler          #+#    #+#             */
/*   Updated: 2026/06/26 10:31:33 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void	init_and_parse(char ***argv, t_stack **a, t_bench *bnch, int *mode)
{
	*a = NULL;
	*mode = 4;
	ft_bzero(bnch, sizeof(t_bench));
	(*argv)++;
	while (**argv && check_flags(**argv, bnch, mode))
		(*argv)++;
	if (**argv)
	{
		init_program(*argv, a);
		normalize_indices(*a);
	}
}

int	main(int argc, char **argv)
{
	t_stack	*a;
	t_stack	*b;
	t_bench	bnch;
	int		mode;
	int		i;

	if (argc < 2)
		return (0);
	i = 1;
	while (i < argc)
	{
		if (argv[i][0] == '\0')
			return (ft_putstr_fd("Error\n", 2), 1);
		i++;
	}
	b = NULL;
	init_and_parse(&argv, &a, &bnch, &mode);
	if (a && !is_sorted(a))
	{
		bnch.disorder = compute_disorder(a);
		execute_strategy(&a, &b, &bnch, mode);
	}
	if (bnch.active)
		print_bench_results(&bnch);
	return (free_stack(&a), 0);
}
