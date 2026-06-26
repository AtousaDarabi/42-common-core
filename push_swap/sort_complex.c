/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sort_complex.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/23 18:16:19 by jukohler          #+#    #+#             */
/*   Updated: 2026/06/26 18:51:23 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	get_max_index_pos(t_stack *b)
{
	int	max_idx;
	int	max_pos;
	int	pos;

	max_idx = -1;
	max_pos = 0;
	pos = 0;
	while (b)
	{
		if (b->index > max_idx)
		{
			max_idx = b->index;
			max_pos = pos;
		}
		pos++;
		b = b->next;
	}
	return (max_pos);
}

void	push_b_to_a(t_stack **a, t_stack **b, t_bench *bnch)
{
	int	max_pos;
	int	size;

	while (*b)
	{
		max_pos = get_max_index_pos(*b);
		size = stack_size(*b);
		if (max_pos <= size / 2)
			while (max_pos--)
				exec_rotate(a, b, 'b', bnch);
		else
			while (max_pos++ < size)
				exec_rev_rotate(a, b, 'b', bnch);
		exec_push(a, b, 'a', bnch);
	}
}

void	strategy_complex(t_stack **a, t_stack **b, t_bench *bnch)
{
	int	bit;
	int	size;
	int	i;

	bit = 0;
	size = stack_size(*a);
	while (bit < 9 && !is_sorted(*a))
	{
		i = 0;
		while (i++ < size)
		{
			if (((*a)->index >> bit) & 1)
				exec_rotate(a, b, 'a', bnch);
			else
				exec_push(b, a, 'b', bnch);
		}
		while (*b)
			exec_push(a, b, 'a', bnch);
		bit++;
	}
}

void	strategy_adaptive(t_stack **a, t_stack **b, t_bench *bnch)
{
	double	disorder;
	int		size;

	size = stack_size(*a);
	if (size <= 5)
	{
		strategy_simple(a, b, bnch);
		return ;
	}
	disorder = compute_disorder(*a);
	if (disorder < 0.2)
		strategy_simple(a, b, bnch);
	else if (disorder < 0.5)
		strategy_medium(a, b, bnch);
	else
		strategy_complex(a, b, bnch);
}

void	execute_strategy(t_stack **a, t_stack **b, t_bench *bnch, int mode)
{
	if (!a || !*a || is_sorted(*a))
		return ;
	if (mode == 1)
		strategy_simple(a, b, bnch);
	else if (mode == 2)
		strategy_medium(a, b, bnch);
	else if (mode == 3)
		strategy_complex(a, b, bnch);
	else if (mode == 4)
		strategy_adaptive(a, b, bnch);
}
